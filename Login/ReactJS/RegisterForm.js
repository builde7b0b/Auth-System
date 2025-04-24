import React, { useState, useEffect, useRef} from 'react';
import { useNavigate } from 'react-router-dom'
import './RegisterForm.css';
import { registerUser } from '../services/api';
import * as yup from 'yup';
import Swal from 'sweetalert2';


const schema = yup.object().shape({
    email: yup.string().email('Invalid email').required('Email is required'),
    password: yup.string().required('Password is required'),
});



function RegisterForm() {
    const [isRegistered, setIsRegistered] = useState(false);
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });

    const [errors, setErrors] = useState({});

    const usernameInputRef = useRef(null); // Create a ref for the username input

    useEffect(() => {
        // Focus on the username input when the component mounts
        usernameInputRef.current.focus();
      }, []);

    const registerUserF = async (e) => {
        e.preventDefault();
        const email = e.target.elements[0].value;
        const password = e.target.elements[1].value;
        const userData = { email, password };

        try {
            await schema.validate(formData, { abortEarly: false });
            const response = await registerUser(userData);
            if (response.status === 200) {
                setIsRegistered(true);
            }
        } catch (error) {
            if (error.response && error.response.status === 409) {
                // User already exists
                Swal.fire({
                  title: 'Registration Failed',
                  text: 'User with this email already exists.',
                  icon: 'error',
                  confirmButtonText: 'OK'
                });
            } else {
                // Other errors
                Swal.fire({
                    title: 'Registration Failed',
                    text: 'An unexpected error occurred.',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
                console.error("Registration failed:", error);
                const validationErrors = {};
                error.inner.forEach((err) => {
                    validationErrors[err.path] = err.message;
                });
            setErrors(validationErrors);
            console.error("Registration Failed", error);
            }
            
            
        }
        registerUser(userData);
    }

    useEffect(() => {
        if (isRegistered) {
            // Notify the user 
            Swal.fire({
                title: 'Registration Successful!',
                text: 'You have successfully registered.',
                icon: 'success',
                confirmButtonText: 'OK'
            })

            navigate('/login');
        }
    }, [isRegistered, navigate]);

    return (
        <div className="register-form-container">
            <div className="register-form">
                <h1>Sign Up</h1>
                <form onSubmit={registerUserF}>
                    <input
                        type="email" ref={usernameInputRef} placeholder="Email" value={formData.email} 
                        onChange={(e) => setFormData({ ...formData, email: e.target.value })} />
                        {errors.email && <div className="error">{errors.email}</div>}
                    <input type="password" placeholder="Password" value={formData.password} 
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })} />
                    {errors.password && <div className="error">{errors.password}</div>}
                    <button type="submit">Sign Up</button>
                </form>
            </div>
        </div>
    );
}

export default RegisterForm;