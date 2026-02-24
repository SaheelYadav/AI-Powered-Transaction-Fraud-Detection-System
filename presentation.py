#!/usr/bin/env python3
"""
🎯 FINAL YEAR PROJECT PRESENTATION
Fraud Transaction Detection Using Machine Learning
Highly Responsive & Animated Presentation System
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
import matplotlib.patches as mpatches
import time
import threading
from datetime import datetime
import random

class FraudDetectionPresentation:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ Fraud Detection Using ML - Final Year Project")
        self.root.geometry("1400x800")
        self.root.configure(bg='#0A1628')
        
        # Presentation state
        self.current_slide = 0
        self.total_slides = 14
        self.animation_running = False
        
        # Color scheme
        self.colors = {
            'bg': '#0A1628',
            'accent': '#FFD700',
            'tech': '#00D4FF',
            'text': '#FFFFFF',
            'subtle': '#8892B0'
        }
        
        # Initialize slides
        self.create_slides()
        
        # Navigation (create before show_slide)
        self.create_navigation()
        self.show_slide(0)
        
    def create_navigation(self):
        """Create navigation controls"""
        nav_frame = tk.Frame(self.root, bg=self.colors['bg'])
        nav_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        
        # Previous button
        prev_btn = tk.Button(
            nav_frame, text="◀ Previous", 
            command=self.prev_slide,
            bg=self.colors['tech'], fg='white',
            font=('Arial', 12, 'bold'),
            relief=tk.FLAT, padx=20, pady=10
        )
        prev_btn.pack(side=tk.LEFT, padx=20)
        
        # Slide counter
        self.slide_label = tk.Label(
            nav_frame, text=f"Slide 1/{self.total_slides}",
            bg=self.colors['bg'], fg=self.colors['text'],
            font=('Arial', 14, 'bold')
        )
        self.slide_label.pack(side=tk.LEFT, expand=True)
        
        # Next button
        next_btn = tk.Button(
            nav_frame, text="Next ▶", 
            command=self.next_slide,
            bg=self.colors['tech'], fg='white',
            font=('Arial', 12, 'bold'),
            relief=tk.FLAT, padx=20, pady=10
        )
        next_btn.pack(side=tk.RIGHT, padx=20)
        
        # Keyboard bindings
        self.root.bind('<Right>', lambda e: self.next_slide())
        self.root.bind('<Left>', lambda e: self.prev_slide())
        
    def show_slide(self, slide_num):
        """Display specific slide"""
        if 0 <= slide_num < self.total_slides:
            self.current_slide = slide_num
            self.slide_label.config(text=f"Slide {slide_num + 1}/{self.total_slides}")
            
            # Clear current slide
            for widget in self.root.winfo_children():
                if widget not in self.root.winfo_children()[-3:]:  # Keep navigation
                    widget.destroy()
            
            # Show slide content
            slide_methods = [
                self.slide_1_title, self.slide_2_problem, self.slide_3_objectives,
                self.slide_4_architecture, self.slide_5_dataset, self.slide_6_preprocessing,
                self.slide_7_features, self.slide_8_models, self.slide_9_pipeline,
                self.slide_10_metrics, self.slide_11_results, self.slide_12_applications,
                self.slide_13_limitations, self.slide_14_conclusion
            ]
            
            if slide_num < len(slide_methods):
                slide_methods[slide_num]()
                
    def next_slide(self):
        """Go to next slide"""
        if self.current_slide < self.total_slides - 1:
            self.show_slide(self.current_slide + 1)
            
    def prev_slide(self):
        """Go to previous slide"""
        if self.current_slide > 0:
            self.show_slide(self.current_slide - 1)
    
    def create_header(self, title, subtitle=""):
        """Create slide header"""
        header_frame = tk.Frame(self.root, bg=self.colors['bg'])
        header_frame.pack(fill=tk.X, pady=(30, 20))
        
        # Title
        title_label = tk.Label(
            header_frame, text=title,
            bg=self.colors['bg'], fg=self.colors['accent'],
            font=('Arial', 28, 'bold')
        )
        title_label.pack()
        
        # Subtitle
        if subtitle:
            sub_label = tk.Label(
                header_frame, text=subtitle,
                bg=self.colors['bg'], fg=self.colors['text'],
                font=('Arial', 16)
            )
            sub_label.pack(pady=(5, 0))
    
    def create_bullets(self, points, delay=0.5):
        """Create animated bullet points"""
        bullet_frame = tk.Frame(self.root, bg=self.colors['bg'])
        bullet_frame.pack(pady=20)
        
        for i, point in enumerate(points):
            bullet = tk.Label(
                bullet_frame, text=f"• {point}",
                bg=self.colors['bg'], fg=self.colors['text'],
                font=('Arial', 16),
                justify=tk.LEFT
            )
            bullet.pack(anchor=tk.W, pady=5)
            
            # Animate appearance
            self.root.after(i * int(delay * 1000), lambda b=bullet: b.config(fg=self.colors['text']))
    
    def slide_1_title(self):
        """Slide 1: Title Slide"""
        self.create_header("Fraud Transaction Detection Using Machine Learning", 
                          "Final Year B.Tech Computer Science Engineering Project")
        
        # Main content frame
        content = tk.Frame(self.root, bg=self.colors['bg'])
        content.pack(expand=True)
        
        # Project info
        info_frame = tk.Frame(content, bg=self.colors['bg'])
        info_frame.pack(side=tk.LEFT, padx=50)
        
        tk.Label(
            info_frame, text="🎯 Real-Time Financial Fraud Detection System",
            bg=self.colors['bg'], fg=self.colors['tech'],
            font=('Arial', 18, 'bold')
        ).pack(pady=10)
        
        tk.Label(
            info_frame, text="🧠 Ensemble ML Approach with Explainable AI",
            bg=self.colors['bg'], fg=self.colors['text'],
            font=('Arial', 16)
        ).pack(pady=5)
        
        tk.Label(
            info_frame, text="⚡ Sub-200ms Response Time",
            bg=self.colors['bg'], fg=self.colors['accent'],
            font=('Arial', 16)
        ).pack(pady=5)
        
        # Student info
        student_frame = tk.Frame(content, bg=self.colors['bg'])
        student_frame.pack(side=tk.RIGHT, padx=50)
        
        tk.Label(
            student_frame, text="👤 Student: [Your Name]",
            bg=self.colors['bg'], fg=self.colors['text'],
            font=('Arial', 16)
        ).pack(pady=5)
        
        tk.Label(
            student_frame, text="👨‍🏫 Guide: [Guide's Name]",
            bg=self.colors['bg'], fg=self.colors['text'],
            font=('Arial', 16)
        ).pack(pady=5)
        
        tk.Label(
            student_frame, text="📅 2024",
            bg=self.colors['bg'], fg=self.colors['accent'],
            font=('Arial', 16, 'bold')
        ).pack(pady=5)
    
    def slide_2_problem(self):
        """Slide 2: Problem Statement"""
        self.create_header("The $32 Billion Fraud Challenge")
        
        # Create matplotlib figure for visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), facecolor=self.colors['bg'])
        fig.patch.set_facecolor(self.colors['bg'])
        
        # Fraud losses over time
        years = [2019, 2020, 2021, 2022, 2023, 2024]
        losses = [22.1, 25.3, 28.1, 30.5, 31.8, 32.0]
        ax1.plot(years, losses, color=self.colors['accent'], linewidth=3, marker='o', markersize=8)
        ax1.fill_between(years, losses, alpha=0.3, color=self.colors['accent'])
        ax1.set_title('Global Fraud Losses ($ Billion)', color='white', fontsize=14)
        ax1.set_xlabel('Year', color='white')
        ax1.set_ylabel('Losses ($ Billion)', color='white')
        ax1.tick_params(colors='white')
        ax1.grid(True, alpha=0.3)
        ax1.set_facecolor('#1A2332')
        
        # Detection time comparison
        methods = ['Traditional', 'Rule-Based', 'Our ML System']
        times = [45, 15, 0.008]  # in days
        colors = ['#FF6B6B', '#FFA500', self.colors['tech']]
        bars = ax2.bar(methods, times, color=colors)
        ax2.set_title('Fraud Detection Time (Days)', color='white', fontsize=14)
        ax2.set_ylabel('Days to Detect', color='white')
        ax2.tick_params(colors='white')
        ax2.set_yscale('log')
        ax2.set_facecolor('#1A2332')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, time in zip(bars, times):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{time:.3f}', ha='center', va='bottom', color='white')
        
        plt.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)
        
        # Key points
        self.create_bullets([
            "Global financial fraud losses exceed $32 billion annually",
            "Traditional systems miss 60% of sophisticated attacks",
            "Average fraud detection time: 45 days (too late for prevention)",
            "Our ML system detects fraud in under 250ms"
        ])
    
    def slide_3_objectives(self):
        """Slide 3: Objectives"""
        self.create_header("Why ML for Fraud Detection?")
        
        # Create target diagram
        fig, ax = plt.subplots(figsize=(10, 8), facecolor=self.colors['bg'])
        fig.patch.set_facecolor(self.colors['bg'])
        ax.set_facecolor(self.colors['bg'])
        
        # Draw target circles
        for i, radius in enumerate([3, 2.5, 2, 1.5, 1]):
            circle = Circle((0, 0), radius, fill=False, 
                          edgecolor=self.colors['subtle'], alpha=0.5-i*0.1)
            ax.add_patch(circle)
        
        # Add objectives in quadrants
        objectives = [
            (-1.5, 1.5, "95% Detection\nRate"),
            (1.5, 1.5, "40% False Positive\nReduction"),
            (-1.5, -1.5, "Real-Time\nProcessing"),
            (1.5, -1.5, "Explainable\nAI")
        ]
        
        for x, y, text in objectives:
            ax.text(x, y, text, ha='center', va='center', 
                   fontsize=12, color='white',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor=self.colors['tech'], alpha=0.7))
        
        # Center target
        ax.text(0, 0, "FRAUD\nDETECTION", ha='center', va='center',
               fontsize=14, fontweight='bold', color=self.colors['accent'])
        
        ax.set_xlim(-4, 4)
        ax.set_ylim(-4, 4)
        ax.set_aspect('equal')
        ax.axis('off')
        
        canvas = FigureCanvasTkAgg(fig, self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)
        
        self.create_bullets([
            "Primary Goal: Reduce false positives by 40% while maintaining 95% detection rate",
            "Technical Objectives: Implement ensemble ML with SHAP explainability",
            "Business Impact: Enable real-time fraud prevention (<200ms response)",
            "Innovation: Combine supervised, unsupervised, and graph-based approaches"
        ])
    
    def slide_14_conclusion(self):
        """Slide 14: Conclusion"""
        self.create_header("Key Achievements & Impact")
        
        # Create achievement visualization
        fig, ax = plt.subplots(figsize=(12, 8), facecolor=self.colors['bg'])
        fig.patch.set_facecolor(self.colors['bg'])
        ax.set_facecolor(self.colors['bg'])
        
        # Achievement badges
        achievements = [
            ("96% RECALL", 0, self.colors['accent']),
            ("94% PRECISION", 1, self.colors['tech']),
            ("250ms RESPONSE", 2, '#4ECDC4'),
            ("PRODUCTION READY", 3, '#FFD700')
        ]
        
        for i, (text, x, color) in enumerate(achievements):
            # Badge circle
            circle = Circle((x*3, 0), 1.2, facecolor=color, alpha=0.8, edgecolor='white', linewidth=2)
            ax.add_patch(circle)
            
            # Achievement text
            ax.text(x*3, 0, text, ha='center', va='center',
                   fontsize=12, fontweight='bold', color='white')
        
        # Success indicator
        ax.text(4.5, 3, "PROJECT COMPLETE", ha='center', va='center',
               fontsize=16, fontweight='bold', color=self.colors['accent'])
        
        ax.set_xlim(-1, 6)
        ax.set_ylim(-2, 4)
        ax.axis('off')
        
        canvas = FigureCanvasTkAgg(fig, self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)
        
        self.create_bullets([
            "Achieved 96% recall with 94% precision in fraud detection",
            "Real-time processing under 250ms per transaction",
            "Explainable AI providing transparent decision-making",
            "Production-ready system with deployment capabilities"
        ])
    
    def create_slides(self):
        """Initialize all slides"""
        pass  # Slides are created dynamically

def main():
    """Main function to run the presentation"""
    root = tk.Tk()
    app = FraudDetectionPresentation(root)
    root.mainloop()

if __name__ == "__main__":
    main()
