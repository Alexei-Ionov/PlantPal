import React, { useContext, useState, useEffect} from 'react';
import { AuthContext } from '../components/AuthContext'; 
import { useNavigate } from 'react-router-dom';
import TokensContainer from '../components/TokensContainer'; 
function Profile() { 
    const { user, logout} = useContext(AuthContext);
    const [userData, setUserData] = useState(null);
    const navigate = useNavigate(); // Get the history instance
    const [errorMsg, setErrorMsg] = useState('');
    const [tokens, setTokens] = useState([]);
    const fetchUserTokens = async () => { 
        setErrorMsg('')
        try { 
            const response = await fetch(`http://127.0.0.1:6969/my_tokens`, { 
                method: 'GET',
                credentials: 'include',
            });
            if (!response.ok) { 
                console.log("Failed to fetch user tokens");
                throw new Error(response.message);
            }
            const tokens = await response.json();
            setTokens(tokens);            
        } catch (err) {
            console.log(err.message);
            setErrorMsg(err.message);
        } 
    };
    
    useEffect(() => { 
        const get_tokens = async () => {
            await fetchUserTokens();
        };
        get_tokens();
    }, []);
    const handleLogoutSubmit = async (event) => { 
        event.preventDefault();
        try { 
            console.log("logging out user");
            await logout(); 
            navigate('/'); //redirect to home page
            console.log("logged user out");
        } catch (err) { 
            console.log(err.message);
        }
    }
    return (
        <div>
            <h1>Profile</h1>
            <br></br>
            <p>Username: {user.username}</p>
            <p>Email: {user.email}</p>
            <p>{errorMsg}</p>
            <br></br>
            <h3>Tokens:</h3>
            {tokens && <TokensContainer tokens={tokens} />}
            <br></br>
            <button onClick={handleLogoutSubmit}>Logout</button>
        </div>
    );
};
export default Profile;