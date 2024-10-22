import React, { useState, useEffect, useTransition } from 'react';
import { Link } from 'react-router-dom';
import '../css/fileMetadata.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUpRightFromSquare } from '@fortawesome/free-solid-svg-icons';


function PlantMetadata({ plant }) {
    const [errorMsg, setErrorMsg] = useState('');
    const [plantInfo, setPlantInfo] = useState({});
    const getPlantInfo = async () => { 
        setErrorMsg('');
        setPlantInfo({});
        try {
            const params = new URLSearchParams({
                plant: `${plant.common_name}`
            })
            const response = await fetch(`https://127.0.0.1:5000/about_plant?${params.toString()}`, { 
                method: 'GET',
                credentials: 'include',
            });
            if (!response.ok) {
                // const message = await response.json();
                throw new Error("Failed to get plant info");
            }
            setPlantInfo(response.json());
            console.log("retrieved plant info");
        } catch (err) { 
            console.log(err);
            setErrorMsg(err.message);
        }
    };
    return (
        <div style={{
          border: '1px solid #ccc',
          backgroundColor: '#fff',
          padding: '20px',
          marginBottom: '20px',
          position: 'relative',
          boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
          borderRadius: '8px',
        }}>
          {plant &&
            <div>
              <div
                style={{
                    textAlign: 'center',
                    margin: '0',
                    position: 'absolute',
                    top: '10px',
                    left: '50%',
                    transform: 'translateX(-50%)',
                    cursor: 'pointer' // Add cursor pointer for visual indication
                }} onClick={getPlantInfo}>About Plant {<FontAwesomeIcon icon={faUpRightFromSquare} />} 
              </div>
              {/* <Link to={`/viewProfile/${file.ownerid}`} className="file-link-style"> Uploaded by {file.owner}</Link> */}
              {/* <h5> {commentCount} Comments</h5> */}
              <button onClick={()=> {
    
                handleViewComments();
                }}>{<FontAwesomeIcon icon={faComment}/>}</button>
              {commentButton && (<CommentBox fileid={file.fileid} parentid={-1} setCommentCount={setCommentCount} setNestedComments={setComments}/>)}
              {commentButton && (<CommentContainer comments={comments} setCommentCount={setCommentCount} fileid={file.fileid}/>)}
            </div>
          }
        </div>
    );
}
export default PlantMetadata;