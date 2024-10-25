import React from 'react';
import TokenMetadata from './TokenMetadata';
function TokensContainer({ tokens }) {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      padding: '20px',
    }}>
      {tokens.map((token) => (
        <div key={token.id} style={{ marginBottom: '20px', width: '100%' }}>
            <TokenMetadata token={token} />
        </div>
      ))}
    </div>
  );
};

export default TokensContainer;
