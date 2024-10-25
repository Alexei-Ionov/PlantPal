import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUpRightFromSquare, faArrowDown } from '@fortawesome/free-solid-svg-icons';
import '../css/PlantMetadata.css'; // CSS for hover effect

function PlantMetadata({ plant }) {
    const [errorMsg, setErrorMsg] = useState('');
    const [plantInfo, setPlantInfo] = useState({});

    const getPlantInfo = async () => {
        setErrorMsg('');
        setPlantInfo({});
        try {
            const params = new URLSearchParams({
                plant: `${plant.common_name}`
            });
            const response = await fetch(`https://127.0.0.1:5000/about_plant?${params.toString()}`, { 
                method: 'GET',
                credentials: 'include',
            });
            if (!response.ok) {
                throw new Error("Failed to get plant info");
            }
            setPlantInfo(response.json());
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
                        About Plant <FontAwesomeIcon icon={faUpRightFromSquare} />
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
                        <div class="plant-status">
                            <p class="moisture-level">Desired Moisture: {plant.desired_soil_moisture}</p>
                            {plant.esp32_ip ? (
                                <h3 class="connection-status">Connected to, {plant.esp32_ip}</h3>
                            ) : (
                                <h3 class="connection-status">Not Connected</h3>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default PlantMetadata;
