import React, { useState } from 'react';

function TokenMetadata({ token }) {

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
            {token && (
                <div style={{ textAlign: 'center' }}>
                 

                    {/* token id */}
                    <h1 style={{
                        margin: '0',
                        fontSize: '2rem',  // Larger nickname
                        fontWeight: 'bold'  // Bold nickname
                    }}>Token: {token.token_id}</h1>
                    {token.esp32_ip ? <h3>Connected to, {token.esp32_ip}</h3> : <h3>Not Connected</h3>}
                
                </div>
            )}
        </div>
    );
}

export default TokenMetadata;
