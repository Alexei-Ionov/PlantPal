import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUpRightFromSquare, faArrowDown } from '@fortawesome/free-solid-svg-icons';
import '../css/PlantMetadata.css'; // CSS for hover effect

function PlantMetadata({ plant }) {
    const [errorMsg, setErrorMsg] = useState('');
    const [successMsg, setSuccessMsg] = useState('');
    const [plantInfo, setPlantInfo] = useState({});
    const [findESP, setFindESP] = useState(false);
    const [espIP, setEspIP] = useState("");
    const handleConnect = async (event) => { 
        event.preventDefault();
        setErrorMsg('');
        setSuccessMsg('');
        try { 
            const response = await fetch(`http://${espIP}:80/connect`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ token: plant.token }),
            });
            if (!response.ok) {
                const err = await response.json();
                console.log(err)
                throw new Error("Failed to connect to esp32");
            }
            console.log("successfully connected!");
            setSuccessMsg("successfully connected!");
    
        } catch (err) { 
            console.log(err);
            setErrorMsg(err);
        }
    }

    const getPlantInfo = async (event) => {
        event.preventDefault();
        if (Object.keys(plantInfo).length !== 0) { 
            setPlantInfo({});
            return
        }

        console.log("fetching plant info");
        setErrorMsg('');
        setPlantInfo({});
        try {
            const params = new URLSearchParams({
                plant: `${plant.common_name}`
            });
            const response = await fetch(`http://127.0.0.1:6969/about_plant?${params.toString()}`, { 
                method: 'GET',
                credentials: 'include',
            });
            if (!response.ok) {
                throw new Error("Failed to get plant info");
            }
            const data = await response.json();
            setPlantInfo(data);
        } catch (err) {
            console.log(err);
            setErrorMsg(err.message);
        }
    };

    const getArrowPosition = (moistureLevel) => {
        const maxMoisture = 10.0;
        const percentage = (moistureLevel / maxMoisture) * 100;
        return `${percentage}%`;
    };

    return (
        <div style={{
            border: '1px solid #ccc',
            backgroundColor: '#2f4f4f',  // Dark green background
            padding: '20px',
            marginBottom: '20px',
            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
            borderRadius: '8px',
            position: 'relative',
            color: 'lightgreen',
            width: '80%',  // Less wide plant div
            margin: '0 auto',  // Center the div
            maxWidth: '600px'  // Max width to control large screens
        }}>
            {plant && (
                <div style={{ textAlign: 'center' }}>
                    {/* About Plant Icon */}
                    <div
                        style={{
                            position: 'absolute',
                            top: '10px',
                            right: '10px',
                            cursor: 'pointer',
                            color: 'lightgreen'
                        }}
                        onClick={getPlantInfo}
                    >
                        About {plant.common_name} <FontAwesomeIcon icon={faUpRightFromSquare} />
                    </div>

                    {/* Nickname */}
                    <h1 style={{
                        margin: '0',
                        fontSize: '2rem',  // Larger nickname
                        fontWeight: 'bold'  // Bold nickname
                    }}>{plant.nickname}</h1>
                    <br></br>
                    {/* Number Line Representation */}
                    <div style={{ marginTop: '20px' }}>
                        <div style={{
                            height: '10px',
                            width: '100%',
                            backgroundColor: '#ddd',
                            position: 'relative',
                            borderRadius: '5px',
                        }}>
                            {/* Enlarged Arrow for desired moisture level */}
                            <div style={{
                                position: 'absolute',
                                left: getArrowPosition(plant.desired_soil_moisture),
                                transform: 'translateX(-50%)',
                                top: '-25px'  // Move it further up
                            }}>
                                <FontAwesomeIcon icon={faArrowDown} color="red" size="2x" />  {/* Increased size */}
                            </div>
                        </div>
                        {/* Labels for moisture level */}
                        <div style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            marginTop: '5px',
                            color: 'white',
                            fontSize: '0.8rem'
                        }}>
                            <span>0.0</span>
                            <span>10.0</span>
                        </div>
                        <div className="plant-status">
                            <p className="moisture-level">Desired Moisture: {plant.desired_soil_moisture}</p>
                            {plant.esp32_ip ? (
                                <h3 className="connection-status">Connected to {plant.esp32_ip}</h3>
                            ) : (
                                <h3 className="connection-status">
                                    
                                    <button 
                                        className="connect-button" 
                                        onClick={() => setFindESP(!findESP)}
                                    >
                                        Connect to ESP32
                                    </button>
                                </h3>
                            )}
                        </div>

                    </div>
                    {Object.keys(plantInfo).length !== 0 && 
                        <div>
                            <h1>ABOUT</h1>
                            {plantInfo.common_name && <h3>Common Name: {plantInfo.common_name}</h3>}
                            {plantInfo.genus && <h3>Genus: {plantInfo.genus}</h3>}
                            {plantInfo.family && <h3>Family: {plantInfo.family}</h3>}
                            {plantInfo.growth_rate && <h3>Growth rate: {plantInfo.growth_rate}</h3>}
                            {plantInfo.average_height &&  <h3>Average Height: {plantInfo.average_height}</h3>}
                            {plantInfo.light && <h3>Optimal Lighting: {plantInfo.light}</h3> }
                            {plantInfo.desired_soil_moisture && <h3>Desired Soil Moisture: {plantInfo.desired_soil_moisture}</h3>}
                            {plantInfo.toxicity && <h3>Toxicity: {plantInfo.toxicity}</h3>}
                            {plantInfo.edible && <h3>Edible: {plantInfo.edible}</h3>}
                            {/* {plantInfo.image_url && <h3>Image url: {plantInfo.image_url}</h3>}                             */}
                        </div>   
                    }
                    {findESP && 
                        <form onSubmit={handleConnect}>
                        <label htmlFor="esp32_ip">ESP32 IP:</label>
                        <input
                          type="text"
                          id="ip"
                          name="ip"
                          value={espIP}
                          onChange={(e) => setEspIP(e.target.value)}
                          required
                        />
                        <br />
                        <br></br>
                        <button type="submit">Connect</button>
                      </form>  
                    }
                    <h3>{successMsg}</h3>
                </div>
                
            )}
        </div>
    );
}

export default PlantMetadata;
