import numpy as np
import json
import random
import pickle
import tkinter as tk
from tkinter import messagebox
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.neighbors import KNeighborsClassifier

def ask_questions_gui():
    """GUI-based career quiz."""
    scores = {key: 0 for key in ["logic", "hardware", "ai", "security", "software", "data", "robotics", "cloud"]}
    
    def submit():
        for key in scores:
            scores[key] = var_dict[key].get()
        career = recommend_career(scores)
        insights = provide_ai_insights(career)
        roadmap = provide_career_roadmap(career)
        messagebox.showinfo("Career Recommendation", f"Based on your answers, a suitable career path for you is: {career}\n\nAI Insights:\n{insights}\n\nRoadmap to Success:\n{roadmap}")
        show_flowchart(career)
        root.destroy()
    
    root = tk.Tk()
    root.title("AI Career Mapping Tool")
    
    questions = [
        ("Do you enjoy problem-solving and logical thinking?", "logic"),
        ("Do you prefer working with hardware over software?", "hardware"),
        ("Do you like designing AI algorithms?", "ai"),
        ("Are you interested in cybersecurity and ethical hacking?", "security"),
        ("Do you enjoy working on web or mobile applications?", "software"),
        ("Do you like working with data analysis and statistics?", "data"),
        ("Do you have an interest in robotics and automation?", "robotics"),
        ("Do you enjoy working with cloud platforms and DevOps?", "cloud")
    ]
    
    var_dict = {}
    for q, key in questions:
        frame = tk.Frame(root)
        frame.pack(anchor='w')
        tk.Label(frame, text=q).pack(side='left')
        var_dict[key] = tk.IntVar()
        tk.Checkbutton(frame, variable=var_dict[key]).pack(side='right')
    
    tk.Button(root, text="Submit", command=submit).pack()
    root.mainloop()

def train_model():
    print("inside train model")
    """Train a KNN model for career recommendation."""
    data = [
        [1, 0, 0, 0, 1, 0, 0, 0, "Software Developer"],
        [1, 1, 0, 0, 0, 0, 0, 0, "Embedded Systems Engineer"],
        [0, 0, 1, 0, 0, 1, 0, 0, "Data Scientist"],
        [0, 0, 1, 1, 0, 1, 0, 0, "AI Researcher"],
        [0, 0, 0, 1, 0, 0, 0, 0, "Cybersecurity Expert"],
        [1, 0, 0, 0, 1, 0, 1, 0, "Robotics Engineer"],
        [0, 0, 0, 0, 0, 0, 0, 1, "Cloud Engineer"]
    ]
    
    X = [row[:-1] for row in data]
    y = [row[-1] for row in data]
    
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(X, y)
    
    with open("career_model.pkl", "wb") as f:
        pickle.dump(model, f)

def recommend_career(scores):
    """AI-based career recommendation using KNN model."""
    with open("career_model.pkl", "rb") as f:
        model = pickle.load(f)
    
    user_input = [[scores[key] for key in scores]]
    prediction = model.predict(user_input)
    return prediction[0]

def provide_ai_insights(career):
    """Provides AI-generated insights for a given career choice."""
    career_descriptions = {
        "Software Developer": "Develops applications and systems using coding languages like Python, Java, and C++.",
        "Embedded Systems Engineer": "Designs specialized computing systems embedded in IoT devices, medical instruments, etc.",
        "Data Scientist": "Analyzes large datasets using statistics and machine learning.",
        "AI Researcher": "Works on cutting-edge AI technologies like deep learning and neural networks.",
        "Cybersecurity Expert": "Protects digital assets from cyber threats and vulnerabilities.",
        "Robotics Engineer": "Designs and develops intelligent robotic systems for automation.",
        "Cloud Engineer": "Specializes in scalable, secure cloud computing platforms."
    }
    
    return career_descriptions.get(career, "No additional insights available.")

def provide_career_roadmap(career):
    """Provides a roadmap to achieving success in the selected career."""
    career_roadmaps = {
        "Software Developer": "1. Learn programming languages (Python, Java, C++).\n2. Build projects and contribute to open-source.\n3. Learn data structures and algorithms.\n4. Gain experience through internships.\n5. Apply for software developer roles.",
        "Data Scientist": "1. Learn Python, SQL, and statistics.\n2. Gain experience in machine learning.\n3. Work with large datasets and tools like Pandas, NumPy.\n4. Build a portfolio with projects.\n5. Apply for data scientist positions.",
        "AI Researcher": "1. Learn Python, deep learning, and ML frameworks.\n2. Understand neural networks and advanced AI concepts.\n3. Contribute to AI research projects.\n4. Publish research papers.\n5. Work in AI development or research labs.",
        "Cybersecurity Expert": "1. Learn networking and security basics.\n2. Get certified (CEH, CISSP).\n3. Gain hands-on experience with ethical hacking tools.\n4. Participate in cybersecurity competitions.\n5. Apply for cybersecurity roles.",
        "Robotics Engineer": "1. Learn C++, Python, and robotics frameworks.\n2. Work with hardware components.\n3. Develop automation projects.\n4. Gain experience in AI and machine learning for robotics.\n5. Apply for robotics engineering positions.",
        "Cloud Engineer": "1. Learn cloud platforms (AWS, Azure, GCP).\n2. Get certified in cloud technologies.\n3. Work on cloud-based projects.\n4. Gain experience in DevOps and containerization.\n5. Apply for cloud engineering roles."
    }
    
    return career_roadmaps.get(career, ["No roadmap available."])
def provide_career_roadmapS(careerS):
    """Provides a roadmap to achieving success in the selected career."""
    career_roadmaps = {
        "Software Developer": ["Learn programming", "Build projects", "Master algorithms", "Gain internships", "Apply for jobs"],
        "Data Scientist": ["Learn Python & SQL", "Master ML concepts", "Work on data projects", "Build portfolio", "Apply for roles"],
        "AI Researcher": ["Learn deep learning", "Understand neural networks", "Work on AI projects", "Publish research", "Join AI labs"],
        "Cybersecurity Expert": ["Learn networking", "Get security certifications", "Practice ethical hacking", "Join security competitions", "Apply for jobs"],
        "Robotics Engineer": ["Learn C++ & Python", "Work on hardware", "Develop automation", "Apply AI in robotics", "Get a robotics job"],
        "Cloud Engineer": ["Learn cloud platforms", "Get certifications", "Build cloud projects", "Gain DevOps experience", "Apply for cloud jobs"]
    }
    
    
    return career_roadmaps.get(careerS, ["No roadmap available."])

def show_flowchart(careerS):
    """Displays a visually enhanced career roadmap flowchart."""
    roadmap = provide_career_roadmapS(careerS)
    G = nx.DiGraph()
    
    numbered_roadmap = [f"{i+1}. {step}" for i, step in enumerate(roadmap)]
    for i in range(len(numbered_roadmap) - 1):
        G.add_edge(numbered_roadmap[i], numbered_roadmap[i + 1])
    
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G, seed=42)
    
    nx.draw(
        G, pos, with_labels=True, node_color='lightcoral', node_size=4000, 
        edge_color='darkblue', font_size=10, font_weight='bold', 
        arrows=True, arrowsize=20, style='dashed'
    )
    
    plt.title(f"{careerS} Roadmap", fontsize=14, fontweight='bold')
    plt.savefig("output.png")  # Save the plot instead of showing it

def main():
    print("inside main")
    train_model()
    ask_questions_gui()

if __name__ == "__main__":
    main()