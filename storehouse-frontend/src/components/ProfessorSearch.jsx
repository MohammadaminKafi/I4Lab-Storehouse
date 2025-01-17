// ProfessorSearch.jsx
import React, { useState, useEffect } from 'react'
import axios from 'axios'

function ProfessorSearch({ setProfessor }) {
  const [professors, setProfessors] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [filteredProfs, setFilteredProfs] = useState([])

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/inventory/professors/')
      .then((response) => {
        setProfessors(response.data)
        setFilteredProfs(response.data)
      })
      .catch((error) => {
        console.error('Error fetching professors:', error)
      })
  }, [])

  useEffect(() => {
    setFilteredProfs(
      professors.filter((p) => {
        const fullName = `${p.first_name} ${p.last_name}`.toLowerCase()
        return fullName.includes(searchTerm.toLowerCase())
      })
    )
  }, [searchTerm, professors])

  return (
    <div>
      <h3>Select Referrer (Professor)</h3>
      <input
        type="text"
        placeholder="Search professor by name"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <div style={{ maxHeight: '200px', overflowY: 'auto', marginTop: '10px' }}>
        <ul style={{ listStyleType: 'none', padding: 0, margin: 0 }}>
          {filteredProfs.map((prof) => (
            <li
              key={prof.professor_id}
              onClick={() => setProfessor(prof)}
              style={{ 
                cursor: 'pointer', 
                margin: '5px 0' 
              }}
            >
              <strong>Prof.</strong> {prof.first_name} {prof.last_name} (ID: {prof.professor_id})
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}

export default ProfessorSearch
