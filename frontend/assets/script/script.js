document.addEventListener("DOMContentLoaded", function () {
    loadSection("header.html", "header", checkAuth); // Ensure header loads before checking auth
    loadSection("footer.html", "footer");
});

// Function to load header or footer dynamically
function loadSection(url, elementId, callback = null) {
    fetch(url)
        .then(response => response.text())
        .then(data => {
            document.getElementById(elementId).innerHTML = data;
            if (callback) callback(); // Run callback after loading content
        })
        .catch(error => console.error(`Error loading ${elementId}:`, error));
}

// ✅ Move functions outside so they are globally accessible
function redirectToLogin() {
    window.location.href = "login.html";
}

function redirectToSignup() {
    window.location.href = "signup.html";
}

function logout() {
    document.cookie = "authToken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    window.location.href = "index.html";
}

function getAuthToken() {
    const cookies = document.cookie.split("; ");
    const tokenCookie = cookies.find(cookie => cookie.startsWith("authToken="));
    return tokenCookie ? tokenCookie.split("=")[1].trim() : null;
}

function checkAuth() {
    const authToken = getAuthToken();
    const authContainer = document.getElementById("auth-buttons-container");

    if (!authContainer) {
        console.error("Auth container not found!"); // ✅ Debugging help
        return;
    }

    if (authToken) {
        console.log("User is logged in, showing logout button"); // ✅ Debugging
        authContainer.innerHTML = `<button class="logout-btn" id="logoutButton">Logout</button>`;
    } else {
        console.log("No auth token found, showing login/signup buttons"); // ✅ Debugging
        authContainer.innerHTML = `
            <button class="login-btn" id="loginButton">Login</button>
            <button class="signup-btn" id="signupButton">Sign Up</button>`;
    }

    // ✅ Attach event listeners after updating UI
    document.getElementById("logoutButton")?.addEventListener("click", logout);
    document.getElementById("loginButton")?.addEventListener("click", () => window.location.href = "login.html");
    document.getElementById("signupButton")?.addEventListener("click", () => window.location.href = "signup.html");
}

// Main script to handle categories and products
document.addEventListener("DOMContentLoaded", function () {
    const categoryGrid = document.querySelector(".category-grid");
    const productList = document.getElementById("product-list");
    const categoryTitle = document.getElementById("category-title");

    const API_URL = "http://127.0.0.1:8000/product/products";

    // Fetch products based on category, limit, and offset
    async function fetchProducts(category, limit, offset) {
        try {
            const response = await fetch(API_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ categories: category, limit: limit, offset: offset }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const products = await response.json();

            if (products.success && Array.isArray(products?.data?.product_id)) {
                displayProducts(products.data.product_id);
            } else {
                console.error("No products found or invalid response:", products);
            }
        } catch (error) {
            console.error("Error fetching products:", error);
        }
    }

    // Render product cards
    function displayProducts(products) {
        productList.innerHTML = "";

        products.forEach(product => {
            const productDiv = document.createElement("div");
            productDiv.classList.add("product-item");
            productDiv.innerHTML = `
                <img src="${product.image_path}" alt="${product.name}" class="product-img" />
                <h3>${product.name}</h3>
                <p>Price: ₹${product.price}</p>
            `;

            productDiv.addEventListener("click", function () {
                openProductPage(product.id);
            });

            productList.appendChild(productDiv);
        });
    }

    // Navigate to product page
    function openProductPage(productId) {
        window.location.href = `product.html?id=${productId}`;
    }

    // Handle category click
    if (categoryGrid) {
        categoryGrid.addEventListener("click", function (e) {
            const categoryDiv = e.target.closest(".category");
            if (categoryDiv) {
                const categoryId = categoryDiv.dataset.id;
                window.location.href = `category.html?category=${categoryId}`;
            }
        });
    }

    // Load featured products (6 random products)
    if (window.location.pathname.includes("index.html")) {
        fetchProducts(null, 6, 5);
    }

    // Load category products on category.html
    function loadCategoryProducts() {
        const params = new URLSearchParams(window.location.search);
        const categoryId = params.get("category");
    
        const categoryTitles = {
            1: "Luxury Watches ",
            2: "Sports Watches",
            3: "Classic Watches"
        };
    
        if (categoryId) {
            const title = categoryTitles[categoryId] || "Products";
            categoryTitle.innerText = title;
            fetchProducts(categoryId, 10, 0);
        }
    }
    
    if (window.location.pathname.includes("category.html")) {
        loadCategoryProducts();
    }
});


// updated codes
document.addEventListener("DOMContentLoaded", function () {
    if (window.location.pathname.includes("product.html")) {
        const urlParams = new URLSearchParams(window.location.search);
        const productId = urlParams.get("id");

        if (productId) {
            fetchProductDetails(productId);
        } else {
            console.error("Product ID not found in URL.");
        }
    }
});

let selectedAttributes = {};

async function fetchProductDetails(productId) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/product/products/${productId}`);
        if (!response.ok) {
            throw new Error(`Failed to fetch product details: ${response.status} ${response.statusText}`);
        }
        const productResponse = await response.json();
        if (!productResponse.success || !productResponse.product) {
            throw new Error("Invalid API response structure");
        }
        const product = productResponse.product;
        const productImage = document.getElementById("productImage");

        productImage.src = product.image_path || "default-image.jpg";
        productImage.setAttribute("data-id", product.id);

        document.getElementById("productName").textContent = product.name;
        document.getElementById("productPrice").innerHTML = `<strong>Price: </strong>₹${product.price}`;
        // document.getElementById("productDescription").textContent = product.details;

        const attributesDiv = document.getElementById("productAttributes");
        attributesDiv.innerHTML = `
            <p>Free Home Delivery Across India</p>
            <p>Genuine Product</p>
            <p>No Return Policy</p>
            <p>1 Year Warranty</p>
            <p>2 Year Free Service and Cleaning</p>
            <p><strong>Specifications:</strong></p>
        `;

        const attributes = ["Case_Material", "Dial_Color", "Strap_Type"];
        attributes.forEach(attr => {
            if (product[attr] && Array.isArray(product[attr])) {
                attributesDiv.innerHTML += `<p><strong>${attr.replace("_", " ")}: </strong>${product[attr].map(item => item.value).join(", ")}</p>`;
            }
        });

        attributesDiv.innerHTML += `<p><strong>Description:</strong> ${product.details}</p>`;

    } catch (error) {
        console.error("Error fetching product details:", error);
    }
}


// cart js code
document.addEventListener("DOMContentLoaded", function () {
    const addToCartBtn = document.getElementById("addToCart");
    if (addToCartBtn) {
        addToCartBtn.addEventListener("click", handleAddToCart);
    }
});

// Handle Add to Cart
function handleAddToCart() {
    const productId = getProductId();
    if (!productId) {
        showToast("Error: Product details missing!", "error");
        return;
    }

    const productData = {
        productId,
        productName: getTextContent("productName"),
        productPrice: getTextContent("productPrice").replace("Price: ₹", ""),
        imagePath: getImageSrc("productImage"),
        attributes: getSelectedAttributes()
    };

    const token = getAuthToken();
    token ? syncCartWithServer(token, productData) : addToLocalCart(productData);
}

// Add to Local Cart (For Guests)
function addToLocalCart(productData) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    // Prevent duplicate entries based on product ID & attributes
    const existingItem = cart.find(item => 
        item.productId === productData.productId && 
        JSON.stringify(item.attributes) === JSON.stringify(productData.attributes)
    );

    if (existingItem) {
        showToast("Product already in cart!", "warning");
    } else {
        cart.push({ ...productData, quantity: 1 });
        localStorage.setItem("cart", JSON.stringify(cart));
        showToast("Product added to cart!", "success");
    }
}

// Sync Cart with Server (For Logged-in Users)
async function syncCartWithServer(token, productData) {
    if (!token) {
        showToast("You must be logged in to add items to cart.", "error");
        return;
    }
    const requestBody = {
        product_id: productData.productId,
        attributes: productData.attributes,
        quantity: 1
    };

    console.log("📦 Sending Request Data:", JSON.stringify(requestBody, null, 2));

    try {
        const response = await fetch("http://127.0.0.1:8000/cart/create/", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json", 
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) throw new Error(`Failed: ${response.statusText}`);

        showToast("Cart updated successfully!", "success");
        localStorage.removeItem("cart"); 
    } catch (error) {
        console.error("❌ Cart sync error:", error);
        showToast("Error syncing cart!", "error");
    }
}

// Get Selected Attributes Dynamically
function getSelectedAttributes() {
    const attributes = {};
    document.querySelectorAll(".attribute-container").forEach(container => {
        const attrName = container.getAttribute("data-attribute");
        const selectedOption = container.querySelector(".option-box.selected");
        if (selectedOption) attributes[attrName] = selectedOption.innerText;
    });
    return attributes;
}

//Utility Functions
function getProductId() {
    return document.getElementById("productImage")?.getAttribute("data-id");
}

function getTextContent(id) {
    return document.getElementById(id)?.textContent || "";
}

function getImageSrc(id) {
    return document.getElementById(id)?.getAttribute("src") || "";
}

function showToast(message, type = "success") {
    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// Auto Sync Cart on Login
async function handleLogin() {
    const token = getAuthToken();
    if (token) {
        await syncCartWithServer(token);
        fetchCart();
        window.location.href = "cart.html";
    } else {
        alert("Login failed or token missing");
    }
}

// Auto Sync Cart When Page Loads (For Logged-in Users)
window.onload = () => {
    const token = getAuthToken();
    if (token) syncCartWithServer(token);
};

// cartbutton feature
function goToCart() {
window.location.href = "cart.html";
}


// cart.html js codes
document.addEventListener("DOMContentLoaded", function () {
    fetchCartItems();
});

function fetchCartItems() {
    const token = getAuthToken();
    if (token) {
        return fetchServerCart(token); // Return the promise
    } else {
        return Promise.resolve(fetchLocalStorageCart()); // Return local storage items
    }
}


function fetchServerCart(token) {
    return fetch("http://127.0.0.1:8000/cart/read/", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success && data.cart && data.cart.data && Array.isArray(data.cart.data)) {
            const cartItems = data.cart.data;
            syncCartWithServer(cartItems); 
            displayCartItems(cartItems);
            return cartItems; // ✅ Return items
        } else {
            console.error("Invalid cart structure:", data);
            return [];
        }
    })
    .catch(error => {
        console.error("Error fetching cart:", error);
        return [];
    });
}



// ✅ Fetch cart from Local Storage (for guests)
function fetchLocalStorageCart() {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    displayCartItems(cart);
}

// ✅ Display cart items on page
// function displayCartItems(items) {
//     const cartContainer = document.getElementById("cart-container");
//     if (!cartContainer) {
//         console.error("Cart container not found!");
//         return;
//     }

//     cartContainer.innerHTML = ""; // Clear cart content

//     if (!Array.isArray(items) || items.length === 0) {
//         cartContainer.innerHTML = "<p>Your cart is empty.</p>";
//         document.getElementById("cart-total").innerText = "0.00"; // Reset total value
//         return;
//     }

//     items.forEach(item => {
//         const cartItem = document.createElement("div");
//         cartItem.classList.add("cart-item");
//         cartItem.setAttribute("data-cart-id", item.cart_item_id);

//         cartItem.innerHTML = `
//             <img src="${item.image_path}" alt="${item.product_name}" class="cart-item-image">
//             <div class="cart-item-details">
//                 <h3 class="product-link" data-id="${item.product_id}">${item.product_name}</h3>
//                 <p>Price: ₹${item.product_price}</p>
//                 <p>Quantity: 
//                     <button class="decrease-btn" data-id="${item.cart_item_id}">-</button>
//                     <span id="quantity-${item.cart_item_id}">${item.quantity}</span>
//                     <button class="increase-btn" data-id="${item.cart_item_id}">+</button>
//                 </p>
//                 <p>Total: ₹<span id="total-${item.cart_item_id}">${(item.product_price * item.quantity).toFixed(2)}</span></p>
//             </div>
//         `;

//         cartContainer.appendChild(cartItem);
//     });

//     // ✅ Restore "Buy Now" button only on cart.html
//     const isCartPage = window.location.pathname.includes("cart.html");
//     if (isCartPage) {
//         const buyNowButton = document.createElement("button");
//         buyNowButton.innerText = "Buy Now";
//         buyNowButton.classList.add("buy-now-btn");
//         buyNowButton.addEventListener("click", function () {
//             window.location.href = "order.html";
//         });

//         cartContainer.appendChild(buyNowButton);
//     }

//     // ✅ Update Total Cart Value after rendering items
//     updateCartTotal(); 

//     // ✅ Handle quantity changes dynamically (Event Delegation)
//     cartContainer.addEventListener("click", async function (event) {
//         const target = event.target;
//         if (!target.classList.contains("increase-btn") && !target.classList.contains("decrease-btn")) return;

//         const cartItemId = target.getAttribute("data-id");
//         let quantityElement = document.getElementById(`quantity-${cartItemId}`);
//         let totalPriceElement = document.getElementById(`total-${cartItemId}`);

//         if (!quantityElement || !totalPriceElement) return;

//         let currentQuantity = parseInt(quantityElement.innerText);
//         let item = items.find(i => i.cart_item_id == cartItemId);

//         if (!item) return;

//         let newQuantity = currentQuantity + (target.classList.contains("increase-btn") ? 1 : -1);
//         if (newQuantity < 0) return; // Prevent negative values

//         // ✅ Update UI Immediately
//         quantityElement.innerText = newQuantity;
//         totalPriceElement.innerText = (newQuantity * item.product_price).toFixed(2);
//         updateCartTotal();

//         // ✅ Call API immediately when quantity changes
//         const success = await updateQuantity(cartItemId, newQuantity);

//         // ✅ If API fails, revert changes
//         if (!success) {
//             quantityElement.innerText = currentQuantity; // Revert UI
//             totalPriceElement.innerText = (currentQuantity * item.product_price).toFixed(2);
//             updateCartTotal();
//             return;
//         }

//         // ✅ If quantity is 0, remove item from UI
//         if (newQuantity === 0) {
//             document.querySelector(`[data-cart-id="${cartItemId}"]`).remove();
//             checkCartEmpty();
//         }
//     });

//     function checkCartEmpty() {
//         if (cartContainer.children.length === 0) {
//             cartContainer.innerHTML = "<p>Your cart is empty.</p>";
//             document.getElementById("cart-total").innerText = "0.00"; // Reset total
//         }
//     }
// }
// perfect one
// function displayCartItems(items) {
//     const cartContainer = document.getElementById("cart-container");
//     if (!cartContainer) {
//         console.error("Cart container not found!");
//         return;
//     }

//     cartContainer.innerHTML = ""; // Clear cart content

//     if (!Array.isArray(items) || items.length === 0) {
//         cartContainer.innerHTML = "<p>Your cart is empty.</p>";
//         document.getElementById("cart-total").innerText = "0.00"; // Reset total value
//         return;
//     }

//     items.forEach(item => {
//         const cartItem = document.createElement("div");
//         cartItem.classList.add("cart-item");
//         cartItem.setAttribute("data-cart-id", item.cart_item_id);

//         cartItem.innerHTML = `
//             <img src="${item.image_path}" alt="${item.product_name}" class="cart-item-image">
//             <div class="cart-item-details">
//                 <h3 class="product-link" data-id="${item.product_id}">${item.product_name}</h3>
//                 <p>Price: ₹${item.product_price}</p>
//                 <p>Quantity: 
//                     <button class="decrease-btn" data-id="${item.cart_item_id}">-</button>
//                     <span id="quantity-${item.cart_item_id}">${item.quantity}</span>
//                     <button class="increase-btn" data-id="${item.cart_item_id}">+</button>
//                 </p>
//                 <p>Total: ₹<span id="total-${item.cart_item_id}">${(item.product_price * item.quantity).toFixed(2)}</span></p>
//             </div>
//         `;

//         cartContainer.appendChild(cartItem);
//     });

//     // ✅ Restore "Buy Now" button only on cart.html
//     const isCartPage = window.location.pathname.includes("cart.html");
//     if (isCartPage) {
//         const token = getAuthToken(); // Check for auth token

//         const buyNowButton = document.createElement("button");
//         buyNowButton.innerText = "Buy Now";
//         buyNowButton.classList.add("buy-now-btn");

//         if (token) {
//             // ✅ Token exists, allow redirection to order page
//             buyNowButton.addEventListener("click", function () {
//                 window.location.href = "order.html";
//             });
//         } else {
//             // ❌ No token, disable button and show message
//             buyNowButton.disabled = true;
//             buyNowButton.style.backgroundColor = "#ccc";
//             buyNowButton.style.cursor = "not-allowed";
//             buyNowButton.title = "Please log in to place an order.";
//             console.error("No authentication token found.");
//         }

//         cartContainer.appendChild(buyNowButton);
//     }

//     // ✅ Update Total Cart Value after rendering items
//     updateCartTotal(); 

//     // ✅ Handle quantity changes dynamically (Event Delegation)
//     cartContainer.addEventListener("click", async function (event) {
//         const target = event.target;
//         if (!target.classList.contains("increase-btn") && !target.classList.contains("decrease-btn")) return;

//         const cartItemId = target.getAttribute("data-id");
//         let quantityElement = document.getElementById(`quantity-${cartItemId}`);
//         let totalPriceElement = document.getElementById(`total-${cartItemId}`);

//         if (!quantityElement || !totalPriceElement) return;

//         let currentQuantity = parseInt(quantityElement.innerText);
//         let item = items.find(i => i.cart_item_id == cartItemId);

//         if (!item) return;

//         let newQuantity = currentQuantity + (target.classList.contains("increase-btn") ? 1 : -1);
//         if (newQuantity < 0) return; // Prevent negative values

//         // ✅ Update UI Immediately
//         quantityElement.innerText = newQuantity;
//         totalPriceElement.innerText = (newQuantity * item.product_price).toFixed(2);
//         updateCartTotal();

//         // ✅ Call API immediately when quantity changes
//         const success = await updateQuantity(cartItemId, newQuantity);

//         // ✅ If API fails, revert changes
//         if (!success) {
//             quantityElement.innerText = currentQuantity; // Revert UI
//             totalPriceElement.innerText = (currentQuantity * item.product_price).toFixed(2);
//             updateCartTotal();
//             return;
//         }

//         // ✅ If quantity is 0, remove item from UI
//         if (newQuantity === 0) {
//             document.querySelector(`[data-cart-id="${cartItemId}"]`).remove();
//             checkCartEmpty();
//         }
//     });

//     function checkCartEmpty() {
//         if (cartContainer.children.length === 0) {
//             cartContainer.innerHTML = "<p>Your cart is empty.</p>";
//             document.getElementById("cart-total").innerText = "0.00"; // Reset total
//         }
//     }
// }


// ✅ Update Total Cart Value

function displayCartItems(items) {
    const cartContainer = document.getElementById("cart-container");
    if (!cartContainer) {
        console.error("Cart container not found!");
        return;
        }

    cartContainer.innerHTML = ""; // Clear cart content

    if (!Array.isArray(items) || items.length === 0) {
        cartContainer.innerHTML = "<p>Your cart is empty.</p>";
        document.getElementById("cart-total").innerText = "0.00"; // Reset total value
        return;
    }

    items.forEach(item => {
        const cartItem = document.createElement("div");
        cartItem.classList.add("cart-item");
        cartItem.setAttribute("data-cart-id", item.cart_item_id);

        // ✅ Show only available attributes
        const attributesHTML = item.attributes ? Object.entries(item.attributes)
            .filter(([key, value]) => value)
            .map(([key, value]) => `<p>${key.replace('_', ' ').toUpperCase()}: ${value}</p>`)
            .join('') : '';

        cartItem.innerHTML = `
            <img src="${item.image_path}" alt="${item.product_name}" class="cart-item-image">
            <div class="cart-item-details">
                <h3 class="product-link" data-id="${item.product_id}">${item.product_name}</h3>
                <p>Price: ₹${item.product_price}</p>
                ${attributesHTML}
                <p>Quantity: 
                    <button class="decrease-btn" data-id="${item.cart_item_id}">-</button>
                    <span id="quantity-${item.cart_item_id}">${item.quantity}</span>
                    <button class="increase-btn" data-id="${item.cart_item_id}">+</button>
                </p>
                <p>Total: ₹<span id="total-${item.cart_item_id}">${(item.product_price * item.quantity).toFixed(2)}</span></p>
            </div>
        `;

        cartContainer.appendChild(cartItem);
    });

    const isCartPage = window.location.pathname.includes("cart.html");
    if (isCartPage) {
        const token = getAuthToken();
        const buyNowButton = document.createElement("button");
        buyNowButton.innerText = "Buy Now";
        buyNowButton.classList.add("buy-now-btn");

        if (token) {
            buyNowButton.addEventListener("click", function () {
                window.location.href = "order.html";
            });
        } else {
            buyNowButton.disabled = true;
            buyNowButton.style.backgroundColor = "#ccc";
            buyNowButton.style.cursor = "not-allowed";
            buyNowButton.title = "Please log in to place an order.";
            console.error("No authentication token found.");
        }

        cartContainer.appendChild(buyNowButton);
    }

    updateCartTotal();

    cartContainer.addEventListener("click", async function (event) {
        const target = event.target;
        if (!target.classList.contains("increase-btn") && !target.classList.contains("decrease-btn")) return;

        const cartItemId = target.getAttribute("data-id");
        let quantityElement = document.getElementById(`quantity-${cartItemId}`);
        let totalPriceElement = document.getElementById(`total-${cartItemId}`);

        if (!quantityElement || !totalPriceElement) return;

        let currentQuantity = parseInt(quantityElement.innerText);
        let item = items.find(i => i.cart_item_id == cartItemId);

        if (!item) return;

        let newQuantity = currentQuantity + (target.classList.contains("increase-btn") ? 1 : -1);
        if (newQuantity < 0) return;

        quantityElement.innerText = newQuantity;
        totalPriceElement.innerText = (newQuantity * item.product_price).toFixed(2);
        updateCartTotal();

        const success = await updateQuantity(cartItemId, newQuantity);

        if (!success) {
            quantityElement.innerText = currentQuantity;
            totalPriceElement.innerText = (currentQuantity * item.product_price).toFixed(2);
            updateCartTotal();
            return;
        }

        if (newQuantity === 0) {
            document.querySelector(`[data-cart-id="${cartItemId}"]`).remove();
            checkCartEmpty();
        }
    });

    function checkCartEmpty() {
        if (cartContainer.children.length === 0) {
            cartContainer.innerHTML = "<p>Your cart is empty.</p>";
            document.getElementById("cart-total").innerText = "0.00";
        }
    }
}


function updateCartTotal() {
    let totalCartValue = 0;

    const cartTotalElement = document.getElementById("cart-total");
    if (!cartTotalElement) {
        console.error("Cart total element not found!");
        return;
    }

    document.querySelectorAll("[id^='total-']").forEach(totalElement => {
        const itemTotal = parseFloat(totalElement.innerText.replace(/[^\d.]/g, ''));
        if (!isNaN(itemTotal)) {
            totalCartValue += itemTotal;
        }
    });

    cartTotalElement.innerText = totalCartValue.toFixed(2);
}


async function updateQuantity(cartItemId, newQuantity) {
    console.log("Updating cart...");

    const token = getAuthToken();
    if (!token) {
        updateLocalStorageCart(cartItemId, newQuantity);
        return true;
    }

    const requestBody = JSON.stringify({ 
        cart_item_id: Number(cartItemId), 
        quantity: Number(newQuantity) 
    });

    console.log("Request Body:", requestBody); 

    try {
        const response = await fetch("http://127.0.0.1:8000/cart/update-quantity", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: requestBody
        });

        const data = await response.json();
        console.log("API Response:", data); 

        if (data.success) {
            console.log("Cart updated successfully");
            return true;
        } else {
            console.error("Error updating cart:", data.message);
            return false;
        }
    } catch (error) {
        console.error("Error updating cart:", error);
        return false;
    }
}

// ✅ Check if cart is empty and update UI
function checkCartEmpty() {
    if (document.querySelectorAll(".cart-item").length === 0) {
        document.getElementById("cart-container").innerHTML = "<p>Your cart is empty.</p>";
    }
}


function updateTotalPrice(cartItemId, quantity, price) {
    document.getElementById(`quantity-${cartItemId}`).innerText = quantity;
    document.getElementById(`total-${cartItemId}`).innerText = `${quantity * price}`;
}


// ✅ Update quantity in Local Storage (for guests)
function updateLocalStorageCart(cartItemId, newQuantity) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    cart = cart.map(item => {
        if (item.cart_item_id === cartItemId) {
            item.quantity = newQuantity;
        }
        return item;
    });

    // ✅ If quantity is zero, remove the item from localStorage
    cart = cart.filter(item => item.quantity > 0);

    localStorage.setItem("cart", JSON.stringify(cart));
    displayCartItems(cart);
}


// address code for order.html 
// updating
document.addEventListener("DOMContentLoaded", function () {
    const addressContainer = document.getElementById("address-container");
    const addAddressBtn = document.getElementById("add-address-btn");
    const addressFormContainer = document.createElement("div");
    addressFormContainer.style.display = "none"; // Initially hidden
    addressContainer.insertAdjacentElement("beforebegin", addressFormContainer);
    
    let editingAddressId = null; // Track address being edited

    addAddressBtn.addEventListener("click", () => {
        editingAddressId = null; // Reset editing mode
        fetchStates();
    });

    function fetchStates(selectedState = "", selectedCity = "") {
        fetch("http://127.0.0.1:8000/location/states/")
            .then(response => response.json())
            .then(states => {
                addressFormContainer.innerHTML = getAddressFormHTML(states, [], selectedState, selectedCity);
                addressFormContainer.style.display = "block";

                document.getElementById("cancel-address-btn").addEventListener("click", () => {
                    addressFormContainer.style.display = "none";
                    editingAddressId = null; // Reset editing mode
                });

                document.getElementById("save-address-btn").addEventListener("click", saveOrUpdateAddress);

                document.getElementById("state").addEventListener("change", function () {
                    fetchCities(this.value);
                });

                if (selectedState) {
                    fetchCities(selectedState, selectedCity);
                }
            })
            .catch(error => console.error("Error fetching states:", error));
    }

    function fetchCities(stateId, selectedCity = "") {
        if (!stateId) return;
    
        fetch("http://127.0.0.1:8000/location/cities/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ state_id: Number(stateId) })
        })
        .then(response => response.json())
        .then(data => {
            const cityDropdown = document.getElementById("city");
            cityDropdown.innerHTML = `<option value="">Select City</option>`;
    
            data.Cities.forEach(city => {
                const option = document.createElement("option");
                option.value = city.id;
                option.textContent = city.name;
                if (city.id == selectedCity) option.selected = true;
                cityDropdown.appendChild(option);
            });
        })
        .catch(error => console.error("Error fetching cities:", error));
    }

    function getAddressFormHTML(states, cities, selectedState = "", selectedCity = "") {
        return `
            <h3>${editingAddressId ? "Update Address" : "Create New Address"}</h3>
            <input type="text" id="name" placeholder="Full Name">
            <input type="text" id="address" placeholder="Address">
            <input type="text" id="landmark" placeholder="Landmark">
            
            <select id="state">
                <option value="">Select State</option>
                ${states.map(state => `<option value="${state.id}" ${state.id == selectedState ? "selected" : ""}>${state.name}</option>`).join('')}
            </select>
    
            <select id="city">
                <option value="">Select City</option>
            </select>
    
            <input type="text" id="country" value="India" disabled>
            <input type="hidden" id="country_id" value="1">
            <input type="text" id="pincode" placeholder="Pincode">
    
            <button id="save-address-btn">${editingAddressId ? "Update Address" : "Save Address"}</button>
            <button id="cancel-address-btn">Cancel</button>
        `;
    }

    function saveOrUpdateAddress() {
        const token = getAuthToken();
        if (!token) {
            alert("Authentication error. Please log in again.");
            return;
        }
    
        const name = document.getElementById("name").value.trim();
        const address = document.getElementById("address").value.trim();
        const landmark = document.getElementById("landmark").value.trim();
        const city_id = document.getElementById("city").value;
        const state_id = document.getElementById("state").value;
        const country = document.getElementById("country").value.trim();
        const pincode = document.getElementById("pincode").value.trim();

        if (!name || !address || !city_id || !state_id || !country || !pincode) {
            alert("Please fill in all required fields.");
            return;
        }

        const addressData = { name, address, landmark, city_id, state_id, country, pincode };

        const requestOptions = {
            method: editingAddressId ? "PUT" : "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(addressData),
        };

        const endpoint = editingAddressId 
            ? `http://127.0.0.1:8000/address/update/${editingAddressId}/`
            : "http://127.0.0.1:8000/address/create/";

        fetch(endpoint, requestOptions)
        .then(response => response.json())
        .then(result => {
            alert(editingAddressId ? "Address updated successfully!" : "Address saved successfully!");
            addressFormContainer.style.display = "none";
            editingAddressId = null; 
            fetchAddresses(); 
        })
        .catch(error => {
            console.error("Error saving/updating address:", error);
            alert("Failed to process request.");
        });
    }

    function fetchAddresses() {
        const token = getAuthToken();
        if (!token) return;

        fetch("http://127.0.0.1:8000/address/read/", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success || !Array.isArray(data.addresses)) {
                addressContainer.innerHTML = "<p>No addresses found.</p>";
                return;
            }
            displayAddress(data.addresses);
        })
        .catch(error => console.error("Error fetching addresses:", error));
    }

    function editAddress(addressId) {
        const token = getAuthToken();
        if (!token) return;
    
        fetch(`http://127.0.0.1:8000/address/read/${addressId}/`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                editingAddressId = addressId; // Ensure ID is set
                fetchStates(data.address.state, data.address.city); // Load states and cities
    
                setTimeout(() => {
                    document.getElementById("name").value = data.address.name;
                    document.getElementById("address").value = data.address.address;
                    document.getElementById("landmark").value = data.address.landmark;
                    document.getElementById("pincode").value = data.address.pincode;
                    document.getElementById("save-address-btn").textContent = "Update Address";
                }, 500); // Delay to ensure form is rendered
            }
        })
        .catch(error => console.error("Error fetching address:", error));
    }
    
    // Fix cancel button issue
    function fetchStates(selectedState = "", selectedCity = "") {
        fetch("http://127.0.0.1:8000/location/states/")
            .then(response => response.json())
            .then(states => {
                addressFormContainer.innerHTML = getAddressFormHTML(states, [], selectedState, selectedCity);
                addressFormContainer.style.display = "block";
    
                document.getElementById("cancel-address-btn").addEventListener("click", () => {
                    addressFormContainer.style.display = "none";
                    editingAddressId = null; // Reset editing mode
                });
    
                document.getElementById("save-address-btn").addEventListener("click", saveOrUpdateAddress);
    
                document.getElementById("state").addEventListener("change", function () {
                    fetchCities(this.value);
                });
    
                if (selectedState) {
                    fetchCities(selectedState, selectedCity);
                }
            })
            .catch(error => console.error("Error fetching states:", error));
    }
    

    function displayAddress(addresses) {
        const pagePath = window.location.pathname;
    
        if (pagePath.includes("order.html")) {
            addressContainer.innerHTML = `
                <h3>Shipping Address</h3>
                <div id="shipping-address">${getAddressListHTML(addresses, "shipping")}</div>
    
                <h3>Billing Address</h3>
                <div id="billing-address">${getAddressListHTML(addresses, "billing")}</div>
            `;
        } else if (pagePath.includes("user.html")) {
            addressContainer.innerHTML = addresses.map(address => `
                <div class="address-card">
                    <p><strong>${address.name}</strong>, ${address.address}, ${address.city}, ${address.state}, ${address.country}, Pincode: ${address.pincode}, Landmark: ${address.landmark}</p>
                    <button class="edit-address-btn" data-id="${address.id}">Edit</button>
                </div>
            `).join('');
    
            document.querySelectorAll(".edit-address-btn").forEach(button => {
                button.addEventListener("click", function () {
                    const addressId = this.getAttribute("data-id");
                    editAddress(addressId);
                });
            });
        } else {
            addressContainer.innerHTML = "<p>No address view configured for this page.</p>";
        }
    }
    
    function getAddressListHTML(addresses, type) {
        if (addresses.length === 0) return "<p>No addresses available.</p>";
    
        return addresses.map(address => `
            <div class="address-card" style="display: flex; align-items: center; gap: 10px;">
                <input type="radio" id="address-${address.id}" name="${type}-address" value="${address.id}">
                <label for="address-${address.id}" style="display: flex; align-items: center; gap: 10px; cursor: pointer; width: 100%;">
                    <p style="margin: 0;">
                        <strong>${address.name}</strong>, ${address.address}, ${address.city}, ${address.state}, ${address.country}, Pincode: ${address.pincode}, Landmark: ${address.landmark}
                    </p>
                </label>
            </div>
        `).join('');
    }

    fetchAddresses();
});



// buy now button
function getSelectedAddressIds() {
    const shippingAddress = document.querySelector('input[name="shipping-address"]:checked');
    const billingAddress = document.querySelector('input[name="billing-address"]:checked');
    const token = getAuthToken()

    if (!token) {
        console.error("No authentication token found.");
        return;
    }

    if (!shippingAddress || !billingAddress) {
        // alert("Please select both shipping and billing addresses.");
        return null;
    }

    return {
        shipping_address_id: shippingAddress.value,
        billing_address_id: billingAddress.value,
    };
}  

function getCartItemIds(items) {
    return items.map(item => item.cart_item_id);
}


document.getElementById("place-order-btn").addEventListener("click", async () => {
    const token = getAuthToken();
    if (!token) {
        alert("Please log in to place an order.");
        return;
    }

    // Fetch cart items from the server
    const cartItems = await fetchCartItems(); 
    // if (!cartItems || cartItems.length === 0) {
    //     alert("Your cart is empty.");
    //     return;
    // }

    // Get selected address IDs (shipping & billing)
    const addressIds = getSelectedAddressIds();
    if (!addressIds) return;

    // Prepare order data
    const orderData = {
        cart_items_ids: getCartItemIds(cartItems),
        shipping_address_id: addressIds.shipping_address_id,
        billing_address_id: addressIds.billing_address_id,
    };

    try {
        const response = await fetch("http://127.0.0.1:8000/payment/create", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
            body: JSON.stringify(orderData),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();
        console.log("Order response:", result);

        if (result.success) {
            alert("Order placed successfully!");
            window.location.href = "index.html";
        } else {
            alert(result.message || "Failed to place order. Please try again.");
        }
    } catch (error) {
        console.error("Error placing order:", error);
        alert("Something went wrong. Please try again.");
    }
});

// buy now button for prod.html page 
// document.getElementById("place-order-btn").addEventListener("click", async () => {
//     const token = getAuthToken();
//     if (!token) {
//         showToast("Please log in to place an order.", "error");
//         return;
//     }

//     const productId = document.getElementById("productImage").getAttribute("data-id");
//     if (!productId) {
//         console.error("Product ID not found!");
//         return;
//     }

//     const productData = {
//         productId,
//         attributes: selectedAttributes,
//         quantity: 1
//     };

//     // Step 1: Create the cart (add product)
//     await syncCartWithServer(token, productData);

//     // Step 2: Fetch updated cart directly
//     const updatedCart = await fetchServerCart(token);

//     if (updatedCart && updatedCart.length > 0) {
//         // Step 3: Redirect to order page
//         window.location.href = "order.html";
//     } else {
//         showToast("Failed to add product to cart. Please try again.", "error");
//     }
// });

document.getElementById("place-order-btn").addEventListener("click", async () => {
    const token = getAuthToken();
    if (!token) {
        showToast("Please log in to place an order.", "error");
        return;
    }

    const productId = document.getElementById("productImage").getAttribute("data-id");
    if (!productId) {
        console.error("Product ID not found!");
        return;
    }

    const productData = {
        productId,
        attributes: selectedAttributes,
        quantity: 1
    };

    // Step 1: Create a temporary cart (just for this product)
    await syncCartWithServer(token, productData);

    // Step 2: Fetch the updated cart (to confirm item was added)
    const updatedCart = await fetchServerCart(token);

    if (updatedCart && updatedCart.length > 0) {
        // Step 3: Redirect to order page with product details (via URL params)
        const queryParams = new URLSearchParams({
            productId: productData.productId,
            quantity: productData.quantity,
            attributes: JSON.stringify(productData.attributes)
        }).toString();

        window.location.href = `order.html?${queryParams}`;
    } else {
        showToast("Failed to add product to cart. Please try again.", "error");
    }
});



// Add to Wishlist button event listener
document.addEventListener("DOMContentLoaded", function () {
    const wishlistButton = document.getElementById("addToWishlist");

    if (wishlistButton) {
        // Get product ID from URL and set it directly on the button
        const urlParams = new URLSearchParams(window.location.search);
        const productId = urlParams.get("id");

        if (productId) {
            wishlistButton.setAttribute("data-id", productId);
            console.log("Wishlist button data-id set to:", productId);
        }

        wishlistButton.addEventListener("click", async function () {
            try {
                const productId = wishlistButton.getAttribute("data-id");

                if (!productId) throw new Error("Product ID is missing.");

                const token = getAuthToken();
                if (token) {
                    const myHeaders = new Headers();
                    myHeaders.append("Content-Type", "application/json");
                    myHeaders.append("Authorization", `Bearer ${token}`);

                    const raw = JSON.stringify({ product_id: productId, isFavourite: true });

                    const requestOptions = {
                        method: "POST",
                        headers: myHeaders,
                        body: raw,
                        redirect: "follow"
                    };

                    const response = await fetch("http://127.0.0.1:8000/wishlist/create", requestOptions);

                    if (!response.ok) throw new Error(`Failed to add to wishlist. Status: ${response.status}`);

                    const result = await response.json();
                    console.log("Added to wishlist:", result);
                    showModal("Product added to your wishlist!");
                } else {
                    showModal("Please log in to use the wishlist feature.");
                }
            } catch (error) {
                console.error("Error adding to wishlist:", error.message);
            }
        });
    }
});

function goToWishlist() {
    const authToken = getAuthToken();
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    if (!authToken) {
        alert("Please log in to view your wishlist.");
        window.location.href = "/login.html";
    } else {
        myHeaders.append("Authorization", `Bearer ${authToken}`);
        fetchWishlist(myHeaders); // Fetch wishlist data only if logged in
        document.getElementById("wishlistSidebar").style.right = "0";
        document.getElementById("wishlistOverlay").style.display = "block";
    }
}

// Close the wishlist sidebar
function closeWishlist() {
    document.getElementById("wishlistSidebar").style.right = "-400px";
    document.getElementById("wishlistOverlay").style.display = "none";
}

// Fetch wishlist products from the API
function fetchWishlist(headers) {
    fetch("http://127.0.0.1:8000/wishlist/allProduct", {
        method: "GET",
        headers: headers
    })
    .then(response => response.json())
    .then(result => renderWishlist(result.wishlist.data))
    .catch(error => console.error("Error fetching wishlist:", error));
}

// Render wishlist items dynamically
function renderWishlist(products) {
    const container = document.getElementById("wishlistContainer");
    if (products.length === 0) {
        container.innerHTML = "<p>Your wishlist is empty.</p>";
        return;
    }

    container.innerHTML = products.map(product => `
        <div class="wishlist-item">
            <img src="${product.image_url}" alt="${product.name}">
            <div>
                <h3>${product.name}</h3>
                <p>$${product.price}</p>
            </div>
            <button onclick="removeFromWishlist(${product.id})">Remove</button>
        </div>
    `).join('');
}

// Redirect to product page
function goToProduct(productId) {
    window.location.href = `http://127.0.0.1:8000/product/products/product.html?id=${productId}`;
}

// Remove product from wishlist
function removeFromWishlist(productId) {
    const authToken = getAuthToken();
    if (!authToken) {
        alert("Session expired. Please log in again.");
        window.location.href = "/login.html";
        return;
    }

    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("Authorization", `Bearer ${authToken}`);

    fetch("http://127.0.0.1:8000/wishlist/delete", {
        method: "DELETE",
        headers: myHeaders,
        body: JSON.stringify({ product_id: productId })
    })
    .then(response => response.json())
    .then(() => fetchWishlist(myHeaders)) // Refresh wishlist after removing item
    .catch(error => console.error("Error removing product:", error));
}

// function goToWishlist() {
// window.location.href = "wishlist.html";
// }



function goToUserPage() {
    window.location.href = 'user.html';
}


// search button
function toggleSearch() {
    const searchBtn = document.getElementById("searchBtn");
    let searchInput = document.getElementById("searchInput");

    if (!searchInput) {
        searchInput = document.createElement("input");
        searchInput.type = "text";
        searchInput.id = "searchInput";
        searchInput.placeholder = "Search for products...";
        searchInput.oninput = searchProducts;
        searchInput.onkeypress = handleKeyPress;
        searchInput.style.marginLeft = "10px";
        searchInput.style.padding = "5px";
        searchInput.style.border = "1px solid #ccc";
        searchInput.style.borderRadius = "5px";

        searchBtn.parentNode.insertBefore(searchInput, searchBtn.nextSibling);
        searchInput.focus();
    }

    let resultsList = document.getElementById("searchResults");
    if (!resultsList) {
        resultsList = document.createElement("div");
        resultsList.id = "searchResults";
        resultsList.className = "results-list";
        searchBtn.parentNode.insertBefore(resultsList, searchInput.nextSibling);
    }
}

function searchProducts() {
    const query = document.getElementById("searchInput").value;
    const resultsList = document.getElementById("searchResults");

    if (query.length === 0) {
        resultsList.innerHTML = "";
        return;
    }

    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const raw = JSON.stringify({
        search_term: query,
        offset: 0,
        limit: 10
    });

    const requestOptions = {
        method: "POST",
        headers: myHeaders,
        body: raw,
        redirect: "follow"
    };

    fetch("http://127.0.0.1:8000/product/products/search", requestOptions)
        .then((response) => response.json())
        .then((result) => {
            if (result.success && result.data.products.length > 0) {
                resultsList.innerHTML = result.data.products.map(product => 
                    `<div onclick="openProduct(${product.id})">
                        ${product.name}
                    </div>`
                ).join('');
            } else {
                resultsList.innerHTML = "<li>No products found</li>";
            }
        })
        .catch((error) => console.error('Error:', error));
}

function handleKeyPress(event) {
    if (event.key === "Enter") {
        const query = document.getElementById("searchInput").value;
        if (query.trim() !== "") {
            window.location.href = `search.html?query=${encodeURIComponent(query)}`;
        }
    }
}

function openProduct(productId) {
    window.location.href = `product.html?id=${productId}`;
}
