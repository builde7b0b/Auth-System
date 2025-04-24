import React, {useState, useEffect, useRef} from 'react';
import './LoginForm.css';
import { loginUser } from '../services/api';
import { useNavigate } from 'react-router-dom'
import { useAuth } from './Context';
import Swal from 'sweetalert2';


function LoginForm() {
// const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();
  const usernameInputRef = useRef(null); // Create a ref for the username input
  const { isLoggedIn, login, logout, setIsLoggedIn, userEmail, setUserEmail } = useAuth();

  // useEffect(() => {
  //   console.log('User Email:', userEmail);
  // }, [userEmail]);

  useEffect(() => {
    // Focus on the username input when the component mounts
    usernameInputRef.current.focus();
  }, []);

const loginUserF = async (e) => {
    e.preventDefault();
    const email = e.target.elements[0].value;
    const password = e.target.elements[1].value;
    const userData = {email, password};
    setUserEmail(email);

    try { 
      const response = await loginUser(userData);
      if(response.data.token) {
        const uniqueToken = response.data.token;
        const userEmail = response.data.email;

        setUserEmail(userEmail);
      }
      if (response.status === 200) {
        login();
        Swal.fire({
          title: 'Success!',
          text: 'You have successfully logged in, redirecting to Dashboard',
          icon: 'success',
          confirmButtonText: 'OK'
        }).then((result) => {
          if (result.value) {
            navigate('/dashboard');
          }
        });
      }
    } catch (error) {
      Swal.fire({
        title: 'Failed!',
        text: 'Your Login Failed, Please check your credentials.',
        icon: 'error',
        confirmButtonText: 'OK'
      })
      console.error("Login Failed", error);
    }
  }

  // useEffect(() => {
  //   if (setIsLoggedIn) {
      
      
  //   }
  // }, [setIsLoggedIn, navigate]);

    return (
        <div className="login-form-container">
        <div className="login-form">
          <h1>Login</h1>
          <form onSubmit={loginUserF}>
            <input type="email" placeholder="Email" ref={usernameInputRef} />
            <input type="password" placeholder="Password" />
            <button type="submit">Login</button>
          </form>
        </div>
      </div>
    );
}

export default LoginForm;