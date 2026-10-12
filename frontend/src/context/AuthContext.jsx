import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(() => {
        const saved = localStorage.getItem('placement_user');
        return saved ? JSON.parse(saved) : {
            name: 'Adwait Sharma',
            email: 'adwait@example.com',
            targetRole: 'Software Engineer',
            isLoggedIn: true
        };
    });

    useEffect(() => {
        localStorage.setItem('placement_user', JSON.stringify(user));
    }, [user]);

    const login = (name, email, targetRole) => {
        setUser({
            name: name || 'Adwait Sharma',
            email: email || 'adwait@example.com',
            targetRole: targetRole || 'Software Engineer',
            isLoggedIn: true
        });
    };

    const logout = () => {
        setUser({
            name: 'Guest User',
            email: 'guest@example.com',
            targetRole: 'Software Engineer',
            isLoggedIn: false
        });
    };

    return (
        <AuthContext.Provider value={{ user, setUser, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
