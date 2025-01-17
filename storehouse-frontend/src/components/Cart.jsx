// Cart.jsx
import React from 'react'

function Cart({ cart, removeFromCart, updateCartItem }) {
  return (
    <div>
      <h3>Your Cart</h3>
      {cart.length === 0 ? (
        <p>No items in cart.</p>
      ) : (
        <ul style={{ listStyleType: 'none', padding: 0 }}>
          {cart.map((item, index) => (
            <li key={index} style={{ marginBottom: '20px' }}>
              <div style={{ marginBottom: '5px' }}>
                <strong>{item.name} (ID: {item.product_id})</strong>
              </div>

              {/* Description input */}
              <label style={{ display: 'block', marginBottom: '5px' }}>
                Description:
                <input
                  type="text"
                  value={item.description}
                  onChange={(e) => updateCartItem(index, 'description', e.target.value)}
                  style={{ 
                    marginLeft: '10px', 
                    width: '80%', 
                    backgroundColor: '#333',
                    color: '#fff',
                    border: '1px solid var(--border-color)',
                    marginTop: '5px'
                  }}
                />
              </label>

              {/* Borrow Due Date input */}
              <label style={{ display: 'block', marginBottom: '5px' }}>
                Borrow Due Date:
                <input
                  type="datetime-local"
                  value={item.borrowDueDate}
                  onChange={(e) => updateCartItem(index, 'borrowDueDate', e.target.value)}
                  style={{ 
                    marginLeft: '10px', 
                    backgroundColor: '#333',
                    color: '#fff',
                    border: '1px solid var(--border-color)',
                    marginTop: '5px'
                  }}
                />
              </label>

              {/* Retrieval Due Date input */}
              <label style={{ display: 'block', marginBottom: '5px' }}>
                Retrieval Due Date:
                <input
                  type="datetime-local"
                  value={item.retrievalDueDate}
                  onChange={(e) => updateCartItem(index, 'retrievalDueDate', e.target.value)}
                  style={{ 
                    marginLeft: '10px', 
                    backgroundColor: '#333',
                    color: '#fff',
                    border: '1px solid var(--border-color)',
                    marginTop: '5px'
                  }}
                />
              </label>

              <button 
                onClick={() => removeFromCart(item.product_id)} 
                style={{ marginTop: '5px' }}
              >
                Remove
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default Cart
