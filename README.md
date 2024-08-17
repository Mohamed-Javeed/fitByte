# FitByte - Health Meets Fun, One Bite at a Time

## Overview

FitByte is an innovative nutritionist app that uses computer vision algorithms to analyze food images and calculate the nutrients and calories they contain. Leveraging deep learning models deployed on Roboflow, FitByte can identify various food types and accurately determine macronutrient content such as calories, proteins, and fats. The app is designed to promote healthier eating habits through a gamified experience, where users earn rewards and XP to enhance their personalized avatars.

## Features

- **Computer Vision-Powered Food Analysis**:
  - Upload images of your meals, and the app identifies the food type and calculates the macronutrient content.
  - Utilizes advanced deep learning models for precise food recognition and nutrient estimation.

- **Gamified Health Tracking**:
  - Users earn XP and food cards based on their eating habits.
  - These rewards can be used to build and enhance a virtual avatar, promoting healthier and stronger characters as users make better food choices.

- **Personalized Avatars**:
  - Each user is provided with a unique avatar that evolves based on the user's dietary habits.
  - The avatar's health and strength improve as users consume nutritious foods and earn more XP.

- **Food Cards and XP System**:
  - Earn food cards by maintaining a balanced diet. These cards provide various benefits to your virtual avatar.
  - Gain XP from your daily food intake, which can be used to unlock new features and improve your avatar's appearance and abilities.

## Installation

1. **Clone the Repository**
   ```
   git clone https://github.com/Mohamed-Javeed/fitByte.git
   ```

2. **Navigate to the Project Directory**
   ```
   cd fitByte
   ```

3. **Install Dependencies**
   Make sure you have `pip` and `virtualenv` installed. Recommended Python version 3.11.4. Then, create a virtual environment and install the required packages:
   ```
   virtualenv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Set Up Roboflow API**
   - The Roboflow api key is already provided in the app files. If you wish to use other vision models, you can proceed with the following steps.
   - Sign up for a [Roboflow](https://roboflow.com/) account.
   - Get your API key and set it in your environment variables or within the views.py file.

6. **Apply Migrations**
   Set up the database by running the migrations:
   ```
   python manage.py migrate
   ```

7. **Run the Server**
   Start the development server:
   ```
   python manage.py runserver
   ```

8. **Access the Application**
   Open your web browser and go to `http://127.0.0.1:8000/` to access the application.

## Project Structure

- **food_analysis/**: Core app handling image processing, food recognition, and nutrient calculation.
  
- **user_profile/**: Manages user profiles, including avatar customization and progress tracking.
  
- **rewards/**: Handles the gamification elements, including food cards and XP distribution.
  
- **dashboard/**: Provides a user interface for tracking food intake, viewing avatar progress, and accessing rewards.
  
- **templates/**: HTML templates for rendering the web pages.

- **static/**: Static files including CSS, JavaScript, and images used in the web interface.

## Usage

1. **Upload Food Images**:
   - Take a picture of your meal and upload it through the app's interface.
   - The app will analyze the image, identify the food items, and calculate the nutritional content.

2. **Track Your Diet**:
   - Monitor your daily intake of calories, proteins, and fats.
   - Use the dashboard to view a summary of your nutritional intake and track your progress over time.

3. **Earn Rewards**:
   - Based on your diet, earn food cards and XP that can be used to enhance your virtual avatar.
   - The healthier your eating habits, the more rewards you earn.

4. **Customize Your Avatar**:
   - Use your earned food cards and XP to unlock new features and upgrade your avatar.
   - Aim for a healthier and stronger avatar by consistently making nutritious food choices.

## Benefits of FitByte

FitByte encourages users to adopt healthier eating habits by making nutrition tracking an engaging and rewarding experience. The gamified elements, including avatars and rewards, motivate users to make better dietary choices, leading to improved overall health. By providing real-time feedback on nutrient intake and rewarding positive habits, FitByte helps users stay on track with their health goals.

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## Contact

For any queries or issues, please reach out via [GitHub Issues](https://github.com/Mohamed-Javeed/fitByte/issues).
