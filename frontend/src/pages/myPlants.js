import React, { useState, useEffect } from 'react';
import PlantsContainer from '../components/PlantsContainer';
function MyPlants() {
    const [userPlants, setUserPlants] = useState([])

    const [desired_moisture, set_desired_moisture] = useState({})
    const [successMsg, setSuccessMsg] = useState('')
    const [errorMsg, setErrorMsg] = useState('')

    const [loadingPlants, setLoadingPlants] = useState(false);

    const fetchPlants = async() => {
        console.log("fetching user plants");
        setLoadingPlants(true);
        try { 
            const response = await fetch("http://127.0.0.1:6969/my_plants", {
                method: 'GET',
                credentials: 'include'
            });
            if (!response.ok) {
                const message = await response.json();
                setErrorMsg(message); 
                throw new Error("Failed to fetch user plants");
            }
            const plants = await response.json();
            setUserPlants(plants);
        } catch (err) { 
            console.log(err)
        } finally {
            setLoadingPlants(false);
        }
    };
    useEffect(() => {
        const get_plants = async () => {
            await fetchPlants();
        };
        get_plants();
    }, [])


    return (
        <div>
            <h1>My plants</h1>
            <br></br>
            {loadingPlants && <h1> Loading plants...</h1> }
            {userPlants.length > 0  && <PlantsContainer plants = {userPlants}/>}
            <br></br>
                
        </div>
    )

};
export default MyPlants;