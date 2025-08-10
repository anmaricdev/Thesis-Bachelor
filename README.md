#  Bachelor's Thesis: Development of Learning Modules for Bin-Packing Algorithms in an Interactive Learning Platform

## Overview
This repository contains my Bachelor's thesis research on **"Entwicklung von Lernmodulen zu Bin-Packing-Algorithmen in einer interaktiven Lernplattform"** (Development of Learning Modules for Bin-Packing Algorithms in an Interactive Learning Platform), conducted at the Frankfurt University of Applied Sciences. The project focuses on creating an automated system for generating educational exercises that help students understand and practice bin packing algorithms.

## Research Objective
The thesis investigates how to **automatically generate comprehensive learning modules** for bin packing algorithms, creating an interactive platform that provides students with varied practice problems. The goal is to develop a scalable system that can generate multiple exercise variants to help students master different aspects of algorithm analysis and optimization.

## Key Research Areas

### 1. **Bin Packing Algorithm Education**
- **Core Algorithms**: Bin Packing Algorithms: Best-Fit, First-Fit, Next-Fit, and Worst-Fit implementations
- **Performance Analysis**: Understanding algorithm efficiency and leftover capacity
- **Educational Exercise Design**: Creating meaningful practice problems for students

### 2. **Automated Exercise Generation**
- **Exercise Variants**: Generating 10+ variations per algorithm type for comprehensive practice
- **Problem Complexity Management**: Balancing difficulty levels for effective learning
- **Visual Learning Support**: Creating diagrams and visualizations to aid understanding

### 3. **Interactive Learning Platform Integration**
- **XML Export System**: Formatting exercises for learning management systems
- **Standardized Exercise Format**: Ensuring compatibility with educational platforms
- **Scalable Content Creation**: Automating the generation of large exercise sets

## Technical Implementation

### **Core Technologies**
- **Python**: Primary development language for algorithm implementation and exercise generation
- **Matplotlib**: Data visualization and exercise image generation
- **XML Generation**: Educational content export system for learning platforms
- **Algorithm Libraries**: Custom implementations of all four bin packing algorithms

### **Key Features**
- **7 Exercise Types**: Comprehensive coverage of bin packing concepts
  - **Exercise 1: Guess the Leftover Items** - Students predict how many items will remain unpacked after applying a specific bin packing algorithm
  - **Exercise 2: Order of Placement** - Students specify the sequence in which items are placed into bins using various bin packing algorithms
  - **Exercise 3: Step-by-Step Algorithm Implementation** - Students simulate the bin packing algorithm step by step, entering the bin states (remaining capacities) after each item is placed
  - **Exercise 4: Which Bin? Online Bin Packing** - Students determine which bin the next item will be placed in using the specified bin packing algorithm
  - **Exercise 5: Guess the Algorithm** - Students identify which bin packing algorithm was used based on the final packed state
  - **Exercise 6: Algorithm Performance Prediction** - Students predict which algorithm will use the fewest bins for a given problem
  - **Exercise 7: Item List Optimization** - Students optimize the order of items to minimize leftover capacity for a given bin packing algorithm
- **Multi-Algorithm Coverage**: Each exercise type covers all four algorithms (Best-Fit, First-Fit, Next-Fit, Worst-Fit)
- **Automated Generation**: Creates multiple variants with different parameters
- **Visual Learning**: Generates PNG images showing algorithm states and results
- **Educational Integration**: XML export compatible with learning management systems

## Repository Structure

```
Thesis-Bachelor/
├── Create_Exercises/          # Exercise generation scripts
│   ├── item_list_optimization.py    # Item optimization exercises
│   ├── guess_the_algorithm.py       # Algorithm identification exercises
│   ├── algorithm_performance_prediction.py  # Performance analysis exercises
│   ├── which_bin.py                 # Bin placement exercises
│   ├── guess_leftover.py            # Leftover calculation exercises
│   ├── implement_algorithm_steps.py # Step-by-step implementation
│   ├── order_of_placement.py        # Placement order exercises
│   ├── BinPackingAlgorithms.py      # Core algorithm implementations
│   ├── Visualization.py             # Matplotlib visualization system
│   └── formatter_to_xml.py         # XML export system
├── Exercise_1/                # Guess the leftover items exercises
├── Exercise_2/                # Order of placement exercises
├── Exercise_3/                # Step-by-step algorithm implementation exercises
├── Exercise_4/                # Which bin placement exercises
├── Exercise_5/                # Algorithm identification exercises
├── Exercise_6/                # Performance prediction exercises
├── Exercise_7/                # Item list optimization exercises
└── README.md                  # This file
```

## Academic Context

### **Institution**
- **University**: Frankfurt University of Applied Sciences (Frankfurt UAS)
- **Program**: Bachelor's Degree in Computer Science (B.Sc.)
- **Thesis Title**: "Entwicklung von Lernmodulen zu Bin-Packing-Algorithmen in einer interaktiven Lernplattform"
- **Language**: German
- **Completion Date**: [Expected: 28.08.2025]

### **Research Methodology**
- **Algorithm Analysis**: Study of bin packing algorithms and their characteristics
- **Educational Design**: Development of effective exercise structures for algorithm learning
- **System Implementation**: Full-stack development of automated exercise generation platform
- **Content Validation**: Ensuring generated exercises are pedagogically sound and mathematically correct

## Key Contributions

1. **Automated Exercise Generation System**: Creates comprehensive practice problems for bin packing algorithms
2. **Multi-Algorithm Coverage**: Supports all four major bin packing algorithms with varied scenarios
3. **Educational Content Automation**: Scalable system for creating large sets of learning materials
4. **Interactive Learning Integration**: XML-based export system for educational platforms

## Research Outcomes

- **7 Exercise Types**: Covering different aspects of bin packing algorithm understanding
- **40+ Exercise Variants**: Multiple variations per exercise type for comprehensive practice
- **Automated Generation System**: Scalable platform for creating educational content
- **Technical Documentation**: Complete implementation and evaluation framework

## Related Publications

*[To be added upon thesis completion]*

## Contributing

This is a research repository for my Bachelor's thesis. While contributions are welcome for educational purposes, please note that this is academic work in progress.

## License

This project is part of academic research. Please respect academic integrity and cite appropriately if using any findings or code.

## Contact

- **Student**: Ante Maric
- **Institution**: Frankfurt University of Applied Sciences
- **Email**: [Your Email]
- **LinkedIn**: [Your LinkedIn]

---

⭐ **Star this repository** if you find the research interesting or useful for your own academic work!

---

*This README represents ongoing research. Final results and conclusions will be available upon thesis completion in Summer 2025.*
