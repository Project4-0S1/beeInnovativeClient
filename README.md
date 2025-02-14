# **Bee Innovative Client App**  
The Bee Innovative Client App runs AI detections and connects to the server.  

## **Setup Instructions**  
Before running the client, you must set up a virtual environment and install dependencies.  

1. **Create a virtual environment**:  
   ```sh
   python3 -m venv ~/client
   ```
2. **Activate the virtual environment**:  
   ```sh
   source ~/client/bin/activate
   ```
3. **Install dependencies**:  
   ```sh
   pip install -r /opt/beeInnovativeClient/requirements.txt
   ```
4. **Run the client app**:  
   ```sh
   python3 /opt/beeInnovativeClient/app.py
   ```

---

# **Branching Strategy for Web App, API Development, and Client**  

## **Overview**  
We follow a feature-based branching strategy to streamline development, ensuring organized collaboration, efficient testing, and smooth integration.  

## **Main Branches**  
- **main**: The stable branch containing production-ready code. Only thoroughly tested changes are merged here.  
- **develop**: The integration branch for ongoing development. All feature branches are merged here after review.  

## **Feature Branch Workflow**  
1. **Branch Naming**: Use clear and consistent names, e.g., `<initials>-<short-description>`.  
2. **Creation**: Branch from `develop` for each new feature.  
3. **Development**: Implement the feature in isolation.  
4. **Testing**: Ensure thorough testing within the feature branch.  
5. **Merging**: Create a pull request to merge the feature branch into `develop`.  

## **Merging Guidelines**  

### **Feature to Develop**  
- Open a Pull Request when the feature is complete.  
- Ensure all tests pass and the code is reviewed.  
- Merge with a **squash commit** to keep history clean.  

### **Develop to Main**  
- Merge into `main` only after rigorous testing on `develop`.  
- Use a **merge commit** to retain the context of changes.  
- Tag releases for versioning.  

### **Conflict Resolution**  
- Resolve conflicts locally before pushing to the branch.  
- Always ensure the branch is up-to-date with its base before merging.  

