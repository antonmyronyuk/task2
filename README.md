# Epidemic simulator  
## Usage
<img src="/readme_images/help.png">

## Algorithms
 1) - simple random (may send more than one package from one node to another, 
 but it does not send packages to itself)  
    - unique random (choose single random unique values, 
    but it does not send packages to itself)
 2) Group random (current node choose random group(neighbours) 
 of elements(excluding current node), so it it does not send packages to itself)
 3) Random from registry (send packages only to nodes which have not received packages yet)  

As you can see below group random is better than simple random.  
Random from registry is ideal, but it requires additional memory.  

<img src="/readme_images/example.png">

## Random from registry
Explanation why there are exactly 5 iterations 
(for 20 nodes which send 4 packages)  

<img src="/readme_images/explanation.png">