import React, { useState } from 'react';
function MyPlants() {
    const [plant, setPlant] = useState('')
    const [nickname, setNickname] = useState('')
    const [desired_moisture, set_desired_moisture] = useState({})
    const [successMsg, setSuccessMsg] = useState('')
    const [errorMsg, setErrorMsg] = useState('')
    const handleSubmit = async (event) => {
        event.preventDefault();
        setSuccessMsg('');
        setErrorMsg('');
        try { 
            const response = await fetch("http://127.0.0.1:5000/add_plant", {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ plant, nickname }),
                credentials: 'include',
            });
            if (!response.ok) {
                const message = await response.json();
                setErrorMsg(message); 
                throw new Error("Failed to create account");
            }
            const data = await response.json();
            console.log(data);
            set_desired_moisture(data);
            setSuccessMsg('Plant Added!');
        } catch (err) { 
            console.log(err.message);
            return 
        }
    };

    return (
        <div>
            <h1>My plants</h1>
            <br></br>
            <form onSubmit={handleSubmit}>
                <label htmlFor="plant">Add Plant:</label>
                <input
                type="text"
                id="plant"
                name="plant"
                value={plant}
                onChange={(e) => setPlant(e.target.value)}
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
                <p>{successMsg}</p>
            </form>
            
        </div>
    )

};
export default MyPlants;