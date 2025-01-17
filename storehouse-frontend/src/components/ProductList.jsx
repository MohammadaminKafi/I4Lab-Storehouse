import React from 'react'

function ProductList({ products, addToCart }) {
  return (
    <div style={{ maxHeight: '400px', overflowY: 'auto', border: '1px solid var(--border-color)', padding: '10px' }}>
      <ul style={{ listStyleType: 'none', margin: 0, padding: 0 }}>
        {products.map((prod) => (
          <li 
            key={prod.product_id} 
            style={{ 
              display: 'flex', 
              justifyContent: 'space-between', 
              alignItems: 'center',
              marginBottom: '10px'
            }}
          >
            {/* Left side: product name and ID */}
            <span>
              <strong>{prod.name}</strong> (ID: {prod.product_id})
            </span>

            {/* Right side: button */}
            <button onClick={() => addToCart(prod)}>Add to Cart</button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default ProductList
