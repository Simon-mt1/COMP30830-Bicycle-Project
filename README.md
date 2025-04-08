# 🚴‍♂️ Dublin Bikes

**Dublin Bikes** is a **fantastic** bike-sharing application that helps you find information about bike stations around Dublin. Whether you're searching for a station to pick up or drop off a bike, **Dublin Bikes** is the perfect application for you! 🎉

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Getting Started](#-getting-started)
  - [✅ Prerequisites](#-prerequisites)
  - [🔧 Installation](#-installation)
  - [⚙️ Configuration](#-configuration)
- [💻 Usage](#-usage)
- [🧪 Testing](#-testing)
- [🤝 Contributing](#-contributing)
- [📧 Contact](#-contact)

---

## ✨ Features

- **User Authentication**: Create an account and log in for a personalized experience.
- **Interactive Map**: View stations across Dublin on a map.
- **Navigation Assistance**: Get station addresses and directions from your current location.
- **Weather Forecast**: Check 24-hour weather information to plan your bike trips.
- **Bike Availability Trends**: Analyze bike availability trends for specific stations.

---

## 🚀 Getting Started

### ✅ Prerequisites

Ensure you have Conda installed before proceeding. You can download it here:

🔗 [Conda Installation Guide](https://www.anaconda.com/docs/getting-started/miniconda/install)

### 🔧 Installation

Follow these steps to set up **Dublin Bikes**:

1. **Create a Conda environment:**

   ```bash
   conda create -n your_env_name python=3.10
   ```

2. **Activate the environment:**

   ```bash
   conda activate your_env_name
   ```

3. **Clone the repository:**

   ```bash
   git clone https://github.com/Simon-mt1/COMP30830-Bicycle-Project.git
   ```

4. **Navigate to the project directory:**

   ```bash
   cd COMP30830-Bicycle-Project
   ```

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### ⚙️ Configuration

To configure the project, create a `.env` file in the root directory and add the following environment variables:

```env
JCDECAUX_API_KEY=your_jcdecaux_apikey
GOOGLE_MAPS_API_KEY=your_google_apikey
OPEN_WEATHER_API_KEY=your_open_weather_apikey

MYSQL_DB_USERNAME=your_db_username
MYSQL_DB_PASSWORD=your_db_password
MYSQL_DB_URL=your_db_url
MYSQL_DB_PORT=your_db_port
MYSQL_DB_NAME=your_db_name
```

---

## 💻 Usage

To run **Dublin Bikes**, follow these steps:

1. **Start the application:**

   ```bash
   python main.py
   ```

2. **Access the application** at `http://localhost:5000` in your browser.

3. **Sign up and log in** to use the app.

4. **Navigate to the map page** via the navigation bar.

#### For more advanced usage, check out the - [Documentation](https://aadhithya-ganesh.github.io/sphinx-test/) .

## 🧪 Testing

Run tests using the following command:

```bash
npm test  # or pytest, etc.
```

---

## 🤝 Contributing

We welcome contributions! 🎉 To contribute, follow these steps:

1. **Fork the repository.**
2. **Create a new branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit your changes:**
   ```bash
   git commit -m "Add your awesome feature"
   ```
4. **Push to the branch:**
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open a pull request.** 🚀

---

## 📧 Contact

For questions or feedback, feel free to reach out:

- **Email**: simonmaybury93@gmail.com 📩
- **GitHub Issues**: [Open an Issue](https://github.com/Simon-mt1/COMP30830-Bicycle-Project/issues) 🐛

---

### 👨‍💻 Made with ❤️ by:

- [Simon](https://github.com/Simon-mt1)
- [Hardhik](https://github.com/hardhik1007-lab)
- [Aadhithya](https://github.com/AadhithyaGanesh)

Happy coding! 🚀
