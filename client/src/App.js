import React, { useEffect, useState } from 'react';
import { Users } from './Users';
import { Pages } from './Pages';

const backend_uri = 'http://127.0.0.1:8000';

function App() {
  const [users, setUsers] = useState([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const size = 5;

  useEffect(() => {
    getUsers(page, size);
  }, [page]);

  const getUsers = (page, size) => {
    fetch(`${backend_uri}/users?page=${page}&size=${size}`)
      .then((resp) => resp.json())
      .then((data) => {
        setUsers(data.items);
        setTotal(data.total);
      });
  };

  return (
    <div className='App'>
      <center>
        <h1>Users</h1>
      </center>
      <Users users={users} />
      <Pages page={page} setPage={setPage} size={size} total={total} />
    </div>
  );
}

export default App;
