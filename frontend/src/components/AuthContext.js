import React, { createContext, useState } from 'react';

const AuthContext = createContext();
const AuthProvider = ({children}) => { 
    const [user, setUser] = useState(null);
    const login = async (loginInfo) => { 
        /* loginInfo -> {email: ***, password: ***} */
        const {email, password} = loginInfo;
        
        try { 
            const response = await fetch('http://127.0.0.1:6969/login', { 
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ email: email, password: password }),
                credentials: 'include',
            });
            if (!response.ok) { 
                const error = await response.text();
                console.log(error);
                return error;
            }
            const userData = await response.json();
            setUser(userData);
            console.log("login successful!");
            return '';
        } catch (err) {
            console.log(err.message);
            throw new Error("Failed to login");
        }
    };
    const logout = async () => { 
        try {
            const response = await fetch('http://127.0.0.1:6969/logout', {
                method: 'POST',
                credentials: 'include',
            });
            const message = await response.text();
            setUser(null);
            console.log(message);
        } catch (err) { 
            console.log(err.message);
        }
    };
    return (
        <AuthContext.Provider value={{user, login, logout}}>{children}</AuthContext.Provider>
    );
};
export {AuthContext, AuthProvider};