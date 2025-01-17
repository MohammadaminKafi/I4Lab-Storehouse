// src/components/ProductSearchBar.jsx
import React, { useEffect, useState } from 'react'
import axios from 'axios'

function ProductSearchBar({ searchTerm, setSearchTerm, categoryFilter, setCategoryFilter }) {
  const [categories, setCategories] = useState([])

  useEffect(() => {
    // Fetch categories from the backend
    axios.get('http://127.0.0.1:8000/inventory/categories/')
      .then((response) => {
        setCategories(response.data)
      })
      .catch((error) => {
        console.error('Error fetching categories:', error)
      })
  }, [])

  return (
    <div>
      <h3>Search Products</h3>
      <input
        type="text"
        placeholder="Search by product name"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <select
        value={categoryFilter}
        onChange={(e) => setCategoryFilter(e.target.value)}
      >
        <option value="">All Categories</option>
        {categories.map((cat) => (
          <option key={cat.category_id} value={cat.category_id}>
            {cat.name}
          </option>
        ))}
      </select>
    </div>
  )
}

export default ProductSearchBar
