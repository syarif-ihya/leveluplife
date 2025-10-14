import { useEffect, useState } from "react";

type User = {
  id: number;
  name: string;
};

function App() {
  const [users, setUsers] = useState<User[]>([]);

  useEffect(() => {
    // panggil API FastAPI
    fetch("http://127.0.0.1:8000/api/users")
      .then((res) => res.json())
      .then((data) => setUsers(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-blue-600">Users from Backend</h1>
      <ul className="mt-4">
        {users.map((u) => (
          <li key={u.id}>
            {u.id}. {u.name}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
