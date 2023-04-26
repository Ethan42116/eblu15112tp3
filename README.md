# eblu15112tp3

1.A short description of the project's name and what it does. 


Math Practice: This project is an AI powered math practice app(I did not write the actual AI, used scikit learn). The user enters the app, which generates a random math problem, and writes the answer using the cursor. The computer will then read the user’s handwriting and check it. Additionally, the computer generated problem will increase in difficulty as the user gets more correct.


Image Generator: Another portion of the project is the AI training image generator, which takes in an image and applies many tiny transformations/distortions to turn one image into many different images (can be hundred). I used an older(more buggy) version of this to generate training images to train my AI in math practice to read negative numbers. 


AI Training Interactive App: The final portion of this project is a basic AI training interactive app, which I used to test how the data is fed into the AI to train. There is not much significance in this app except to serve as an intermediate step to help me understand how to format data to feed into AI.




2.How to run the project. 


Note:Please run the everything from the github repo since it contains the training images for the math game to work. Otherwise it would crash


Math Practice: run Math_Game_Front_End.py. 


Image Generator: run Image_Generator.py, also, make sure whatever image you are inputting is in the same folder as Image_Generator.py (I attached many sample images in folder that you can input, such as letter-q.png)


AI Training Interactive App: run AI_Basic_Front_End.py, also make sure all the folders containing your input images are in the same folder as AI_Basic_Front_End.py (I attached many sample training data in folder that you can input, such as training_setA)






3.Which libraries you're using that need to be installed, if any. 


External libraries: PIL, numpy, emnist, matplotlib, sklearn


4.A list of any shortcut commands that exist. Shortcut commands can be used to demonstrate specific features by skipping forward in a game or loading sample data. They're useful for when you're testing your code too!


Math app: press k to see the space finder algorithm work to break your writing into individual characters and convert them to AI readable format

 
