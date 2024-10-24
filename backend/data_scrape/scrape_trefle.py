import os
import aiohttp
import asyncio
import heapq
import time
from dotenv import load_dotenv
import json
# Load environment variables from .env file
load_dotenv()

#unfortantely, we max out at two tokens bc not enough file descripetors available
TOKEN1 = os.getenv('TREFLE_API_KEY1')
TOKEN2= os.getenv('TREFLE_API_KEY2')



COMMON_NAMES = []
FAILED_PAGES = []
FREE = 0
REQUEST_IN_FLIGHT = 1
REQUEST_FAILED_NO_RETRY = -3
REQUEST_FAILED_RETRY = {-1, -2}
PAGE = 1
MAX_PAGE = 21863
WINDOW_SIZE = 120


async def get_data(token_heap, request_state, index, token, lock):
    state, page = request_state
    request_url = f"http://trefle.io/api/v1/plants?token={token}&page={page}"
   
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(request_url) as response:
                if response.status != 200:
                    print(response)
                    raise Exception(f"Failed to retieve data for page: {page}")
                plants = await response.json()
                names = []
                for plant in plants:
                    if plant["common_name"]:
                        names.append(plant["common_name"].lower())
                print(f"Successfully retrieved data for page: {page}")
                return (names, state, index, page)
        except Exception as e:
            print(e)
            return (None, state, index, page)
        finally: 
            # Acquire the lock to safely push to the heap
            async with lock:
                heapq.heappush(token_heap, time.time() + 60)

async def process_tasks(tasks, request_states, final):
    """
    final helps us determine whether we are doing this at the very end of our scrape 
    """
    # Clean up completed tasks
    global REQUEST_IN_FLIGHT
    global REQUEST_FAILED_NO_RETRY
    global REQUEST_FAILED_RETRY
    global FREE
    global COMMON_NAMES
    global FAILED_PAGES
    try: 
        if not tasks:
            return 
        if final: 
            completed, _ = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
        else:
            completed, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        completed = list(completed)
        for task in completed:
            if task.result() is None:
                continue
            names, state, index, page = task.result()  # Get the result of the completed task
            if not names:
                #state here represents the state before it went in-flight
                if state == FREE:
                    request_states[index][0] = -1  #retry
                elif state in REQUEST_FAILED_RETRY:
                    request_states[index][0] -= 1

                    if request_states[index][0] == REQUEST_FAILED_NO_RETRY:
                        FAILED_PAGES.append(page)
                        request_states[index][0] = FREE
            else:
                request_states[index][0] = FREE
                COMMON_NAMES.extend(names)
        # Clean up completed tasks from the task list
        tasks[:] = [task for task in tasks if not task.done()]
    except Exception as e:
        print(e)    
def setup_trie(trie):
    global COMMON_NAMES
    for name in COMMON_NAMES:
        if name is not None:
            
            head = trie
            for letter in name:
                if letter not in head:
                    head[letter] = {}
                head = head[letter]
            if '*' not in head:
                head["*"] = ""
    COMMON_NAMES = []
def create_tasks(token_heap, curr_token, request_states, tasks, lock):
    global REQUEST_IN_FLIGHT
    global REQUEST_FAILED_NO_RETRY
    global REQUEST_FAILED_RETRY
    global FREE
    global PAGE
    global MAX_PAGE
    global WINDOW_SIZE

    current_time = time.time()
    while token_heap and current_time >= token_heap[0] and PAGE <= MAX_PAGE:
        sent = False
        heapq.heappop(token_heap)
        for index in range(len(request_states)):
            state, page_num = request_states[index]
            if state == FREE:
                request_states[index][1] = PAGE
                task = asyncio.create_task(get_data(token_heap, request_states[index], index, curr_token, lock))
                request_states[index][0] = REQUEST_IN_FLIGHT
                tasks.append(task)  
                PAGE += 1
                sent = True
                break

            elif state in REQUEST_FAILED_RETRY:
                print("retrying failed request")
                task = asyncio.create_task(get_data(token_heap, request_states[index], index, curr_token, lock)) #retry failed request
                tasks.append(task)
                request_states[index][0] = REQUEST_IN_FLIGHT
                sent = True
                break  

        if not sent:    #if none of our previous requests have come back yet, we can increase the size of our requets states array
            request_states.append([FREE, PAGE])
            index = len(request_states) - 1
            task = asyncio.create_task(get_data(token_heap, request_states[index], index, curr_token, lock))
            request_states[index][0] = REQUEST_IN_FLIGHT
            tasks.append(task)
            PAGE += 1
        
    return PAGE

async def request_manager():
    """
    - Trefle has 21863 max pages we can query
    
    - RATE LIMIT IS 120 requests / minute !

    - We will use a min heap to keep track of the least recent sent request 
    and an array to keep track of the status' of the 120 (+) possible ongoing requests

    - Ongoing requests will be represented as an array of tuples with the possible valid states (state, page_number):
        0 ->  FREE (ready to send request, initially we will have all zeros)
        1 ->  REQUEST IN FLIGHT 
        -2 <= x <= -1 -> REQUEST FAILED, retry (error server side or possible network error)
        -3 -> REQUESt FAILED, no retry
    e.g. (1, 20) represents that the request for page 20 is currently in flight 

    - we will allow up to 3 retries in terms of resending failed requests. afterwords, we mark them as free and move on 
    """
  
    MINUTE = 60
    global MAX_PAGE
    global REQUEST_IN_FLIGHT
    global REQUEST_FAILED_NO_RETRY
    global REQUEST_FAILED_RETRY
    global FREE
    global PAGE
    global WINDOW_SIZE
    TRIE = {}
    lock1 = asyncio.Lock()
    lock2 = asyncio.Lock()

    current_time = time.time()
    token_heap1 = [current_time for _ in range(WINDOW_SIZE)]  #(time, token for this request)
    token_heap2 = [current_time for _ in range(WINDOW_SIZE)]
    request_states = [[FREE, None] for _ in range(WINDOW_SIZE * 2)] 
    tasks = []
    while PAGE <= MAX_PAGE:
        PAGE = create_tasks(token_heap1, TOKEN1, request_states, tasks, lock1)
        PAGE = create_tasks(token_heap2, TOKEN2, request_states, tasks, lock2)

        setup_trie(TRIE) #kill some time 
    
        await process_tasks(tasks, request_states, final=False)
    await process_tasks(tasks, request_states, final=True)

    print("finishing trie setup...")
    setup_trie(TRIE)

    # Write the dictionary to a JSON file
    with open('trie.json', 'w') as json_file:
        json.dump(TRIE, json_file)


    print("FINISHED SCRAPING")
    # Get the size of the file in bytes
    file_size = os.path.getsize('./trie.json')
    print(f"File size: {file_size} bytes")
   
            

if __name__ == "__main__":
    print("setting up scraper ...")
    # Run the event loop
    asyncio.run(request_manager()) 
    