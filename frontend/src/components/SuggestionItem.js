import React from 'react';
import '../css/SuggestionItem.css'; // CSS for hover effect

const SuggestionItem = ({ suggestion, onSelect }) => {
    return (
        <div className="suggestion-item" onClick={() => onSelect(suggestion)}>
            <h1>{suggestion}</h1>
        </div>
    );
};

export default SuggestionItem;
