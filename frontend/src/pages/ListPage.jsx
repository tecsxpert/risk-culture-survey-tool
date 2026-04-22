import { useEffect, useState } from "react"
import axios from "axios"

function ListPage() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)

 useEffect(() => {
  setTimeout(() => {
    setData([
      { id: 1, name: "Risk 1", status: "Open" },
      { id: 2, name: "Risk 2", status: "Closed" },
    ])
    setLoading(false)
  }, 1000)
}, [])
  if (loading) {
    return <p>Loading...</p>
  }

  if (data.length === 0) {
    return <p>No data available</p>
  }

  return (
    <table border="1" className="mt-5">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {data.map((item) => (
          <tr key={item.id}>
            <td>{item.id}</td>
            <td>{item.name}</td>
            <td>{item.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}

export default ListPage