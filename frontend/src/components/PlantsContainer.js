import React from 'react';
import PlantMetadata from '../components/PlantMetadata';
function PlantsContainer({ plants }) {
  return (
    <div  style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      backgroundColor: '#f9f9f9',
      padding: '20px',
    }}>
      {plants.map((plant) => (
        
        <div key={plant.id} style={{ marginBottom: '20px', width: '100%' }}>
            {
                <PlantMetadata plant={plant}/>
            }
        
        </div>
      ))}
    </div>
  );
}

export default PlantsContainer;