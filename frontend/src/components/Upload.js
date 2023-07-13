import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FormGroup, FormControl, Button } from 'react-bootstrap';
import { API_BASE_URL } from '../config';
import history from '../history';

function Upload() {
  const [file, setFile] = useState()

  const [amount, setAmount] = useState(0);
  const [recipient, setRecipient] = useState('');
  const [knownAddresses, setKnownAddresses] = useState([]);


  
 function handleChange(event) {
    setFile(event.target.files[0])
  }
  useEffect(() => {
    fetch(`${API_BASE_URL}/known-addresses`)
      .then(response => response.json())
      .then(json => setKnownAddresses(json));
  }, []);

  const updateRecipient = event => {
    setRecipient(event.target.value);
  }

  const updateAmount = event => {
    setAmount(Number(event.target.value));
  }

  const submitTransaction = () => {
    fetch(`${API_BASE_URL}/wallet/transact`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ recipient, amount })
    }).then(response => response.json())
      .then(json => {
        console.log('submitTransaction json', json);

        alert('Success!');

        history.push('/transaction-pool');
      });
  }

  return (
    <div className="Upload">
      <Link to="/">Home</Link>
      <hr />
      <h1>Test Upload</h1>
      <br />
      <FormGroup>
      <form>
          
          <input type="file" />
          <button type="submit">Upload </button>
         
        </form>
      </FormGroup>
      
      <div>
       
      </div>
      <br />
       
    </div>
  )
}

export default Upload;
