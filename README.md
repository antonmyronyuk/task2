# Epidemic simulator  
## Usage
<img src="/readme_images/help.png">

## Algorithms
 1) - simple random (may send more than one package from one node to another)  
    - unique random (may send package to itself)
 2) Group random (may send package to itself)
 3) Random from registry  

As you can see below group random is better than simple random.  
Random from registry is ideal, but it requires additional memory.  

<img src="/readme_images/example.png">

## Random from registry
Explanation why there are exactly 5 iterations 
(for 20 nodes which send 4 packages)  

<img src="/readme_images/explanation.png">