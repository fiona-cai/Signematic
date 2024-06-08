// Importing necessary libraries
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

// Creating a scene
const scene = new THREE.Scene();

// Creating a camera
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;

// Creating a renderer
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Adding controls
const controls = new OrbitControls(camera, renderer.domElement);

// Creating a geometry
const geometry = new THREE.SphereGeometry(0.1, 32, 32);

// Creating a material
const material = new THREE.MeshBasicMaterial({ color: 0xffff00 });

// Creating a sphere (hand landmark)
const sphere = new THREE.Mesh(geometry, material);
scene.add(sphere);

// Loading hand landmark data
fetch('hand_landmarks.json')
  .then(response => response.json())
  .then(data => {
    // Setting up animation
    let frame = 0;
    function animate() {
      requestAnimationFrame(animate);

      // Updating hand landmark position
      if (frame < data.length) {
        sphere.position.set(data[frame].x, data[frame].y, data[frame].z);
        frame++;
      }

      controls.update();
      renderer.render(scene, camera);
    }
    animate();
  });