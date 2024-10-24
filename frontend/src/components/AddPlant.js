import React, { useState, useEffect } from 'react';
function AddPlant() { 
    const [plant, setPlant] = useState('')
    const [nickname, setNickname] = useState('')
    const [successMsg, setSuccessMsg] = useState('')
    const [errorMsg, setErrorMsg] = useState('')
    const [loadingMsg, setLoadingMsg] = useState('')
    const [trie, setTrie] = useState({})
    const [suggestions, setSuggestions] = useState([]);
    const SUGGESTION_LIMIT = 10;
    const recurseTrie = (root, prefix) => { 
        if (suggestions.length >= SUGGESTION_LIMIT) { 
            return;
        }
        // If the end of a word is found, add it to the suggestions list
        if (root.hasOwnProperty("*")) { 
            suggestions.push(prefix);  // 'setSuggestions' is not valid in this context
        }
        // Iterate over each letter in the current node
        for (const letter in root) { 
            if (letter !== "*") {  // Avoid treating the '*' key as a child node
                recurseTrie(root[letter], prefix + letter);
            }
        }
    }

    const getSuggestions = (event) => { 
        event.preventDefault();


    }

    const fetchTrie = async () => { 
        try { 
            setLoadingMsg('Loading search engine...');
            const response = await fetch("http://127.0.0.1:5000/fetch_trie", {
                method: 'GET',
                credentials: 'include',
            });
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.message);
            }
            const trie = await response.json();
            setTrie(trie)
            console.log("successfully retrieved trie");
            setSuccessMsg("retrieved trie!");
        } catch (err)  {
            console.log(err);
            setErrorMsg(errorMsg);
        } finally {
            setLoadingMsg('')
        }
    };

    useEffect(() => {
        const get_trie = async () => {
            await fetchTrie();
        };
        get_trie();
    }, [])

    const handleSubmit = async (event) => {
        event.preventDefault();
        setSuccessMsg('');
        setErrorMsg('');
        try { 
            const response = await fetch("http://127.0.0.1:5000/add_plant", {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ plant: plant, nickname: nickname }),
                credentials: 'include',
            });
            if (!response.ok) {
                const message = await response.json();
                setErrorMsg(message); 
                throw new Error("Failed to add plant");
            }
            const data = await response.json();
            console.log(data);
            // set_desired_moisture(data);
            setSuccessMsg('Plant Added!');
        } catch (err) { 
            console.log(err.message);
            return 
        }
    };
    return (
        <form onSubmit={handleSubmit}>
        <label htmlFor="plant">Add Plant:</label>
        <input
        type="text"
        id="plant"
        name="plant"
        value={plant}
        onChange={(e) => 
                    getSuggestions(e.target.value)
                }
        required
        />
        <br />
        <label htmlFor="nickname">Nickname:</label>
        <input
        type="text"
        id="nickname"
        name="nickname"
        value={nickname}
        onChange={(e) => setNickname(e.target.value)}
        required
        />
        <br />
        <button type="submit">Add plant</button>
        <br></br>
        <p>{loadingMsg}</p>
        <p>{successMsg}</p>
        <p>{errorMsg}</p>

    </form>
    );
};
export default AddPlant;