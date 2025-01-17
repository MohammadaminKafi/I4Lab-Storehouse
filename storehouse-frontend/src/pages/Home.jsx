// src/pages/Home.jsx
import React, { useState, useEffect } from 'react'
import axios from 'axios'
import ProductSearchBar from '../components/ProductSearchBar'
import ProductList from '../components/ProductList'
import Cart from '../components/Cart'
import ProfessorSearch from '../components/ProfessorSearch'
import './Home.css'

function Home() {
  const [studentNumber, setStudentNumber] = useState('')
  const [products, setProducts] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [categoryFilter, setCategoryFilter] = useState('')
  const [cart, setCart] = useState([])
  const [professor, setProfessor] = useState(null)

  // Fetch available products
  useEffect(() => {
    axios.get('http://127.0.0.1:8000/inventory/available-products/')
      .then((response) => {
        setProducts(response.data)
      })
      .catch((error) => {
        console.error('Error fetching products:', error)
      })
  }, [])

  // Add product to cart with default fields
  const addToCart = (product) => {
    setCart((prevCart) => [
      ...prevCart,
      {
        ...product,
        description: '',
        borrowDueDate: '',
        retrievalDueDate: '',
      }
    ])
  }

  // Remove from cart
  const removeFromCart = (productId) => {
    setCart((prevCart) => prevCart.filter((p) => p.product_id !== productId))
  }

  // Update cart item fields
  const updateCartItem = (index, field, value) => {
    setCart((prevCart) => {
      const newCart = [...prevCart]
      newCart[index] = { ...newCart[index], [field]: value }
      return newCart
    })
  }

  // Filter logic
  const filteredProducts = products.filter((product) => {
    const matchesName = product.name
      .toLowerCase()
      .includes(searchTerm.toLowerCase())
    const matchesCategory = categoryFilter
      ? product.category === parseInt(categoryFilter)
      : true
    return matchesName && matchesCategory
  })

  // Validate and submit
  const handleSubmitRequest = () => {
    // Basic validation for student number
    if (!studentNumber.trim()) {
      alert('Please enter your student number.')
      return
    }

    if (!professor) {
      alert('Please select a professor before submitting.')
      return
    }

    // Build payload
    const payload = {
      student_number: studentNumber,
      professor_id: professor.professor_id,
      products: cart.map((item) => ({
        product: item.product_id,
        borrow_due_date: item.borrowDueDate || '2025-01-20T10:00:00Z',
        retrieval_due_date: item.retrievalDueDate || '2025-01-30T10:00:00Z',
        description: item.description || 'Requested via the React frontend',
      })),
    }

    // POST request
    axios.post('http://127.0.0.1:8000/inventory/create-request/', payload)
      .then((res) => {
        alert('Request submitted successfully!')
        setCart([])
      })
      .catch((err) => {
        console.error('Error submitting request:', err)
        alert('Error submitting request.')
      })
  }

  return (
    <div className="main-container">
      {/* Left side */}
      <div className="left-section">
        <h2>Cart</h2>

        {/* Student Number */}
        <div style={{ marginBottom: '1rem' }}>
          <label style={{ display: 'block', marginBottom: '0.5rem' }}>
            Student Number:
          </label>
          <input
            type="text"
            value={studentNumber}
            onChange={(e) => setStudentNumber(e.target.value)}
            style={{ 
              width: '100%',
              backgroundColor: '#333',
              color: '#fff',
              border: '1px solid var(--border-color)',
              padding: '0.5rem'
            }}
          />
        </div>

        {/* Show selected professor */}
        <div style={{ marginBottom: '1rem' }}>
          {professor ? (
            <div>
              <strong>Selected Professor:</strong><br />
              Prof. {professor.first_name} {professor.last_name} (ID: {professor.professor_id})
            </div>
          ) : (
            <p>No professor selected.</p>
          )}
        </div>

        <Cart 
          cart={cart} 
          removeFromCart={removeFromCart} 
          updateCartItem={updateCartItem}
        />

        <button className="submit-button" onClick={handleSubmitRequest}>
          Submit Request
        </button>
      </div>

      {/* Right side */}
      <div className="right-section">
        <h2>Search & Select</h2>
        <ProfessorSearch setProfessor={setProfessor} />
        <ProductSearchBar
          searchTerm={searchTerm}
          setSearchTerm={setSearchTerm}
          categoryFilter={categoryFilter}
          setCategoryFilter={setCategoryFilter}
        />
        <ProductList products={filteredProducts} addToCart={addToCart} />
      </div>
    </div>
  )
}

export default Home
