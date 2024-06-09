import * as THREE from 'https://cdn.skypack.dev/three@0.132.2';

var container = document.getElementById("ASL-Gestures");

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x000000);
const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);

const renderer = new THREE.WebGLRenderer();
renderer.setSize(container.clientWidth, container.clientHeight);
container.appendChild(renderer.domElement);

var sentenceList = []
var sentenceIndex = 0;
var wordIndex = 0;
var frameIndex = 0;

fetch("subtitles-1.txt")
  .then((res) => res.text())
  .then((text) => {
    console.log(text);
    sentenceList = text.split(";");

    fetch('hand_landmarks.json')
  .then(response => response.json())
  .then(data => {
    function drawPoint(x, y, z) {
      const pointRadius = 0.25;
      const geometry = new THREE.SphereGeometry(pointRadius, 32, 16);
      const material = new THREE.MeshBasicMaterial({ color: 0xffffff });
      const sphere = new THREE.Mesh(geometry, material);
      sphere.position.x = x;
      sphere.position.y = y;
      sphere.position.z = z;
      scene.add(sphere);
    }

    function drawLine(x1, y1, z1, x2, y2, z2) {
      const points = [];
      points.push(new THREE.Vector3(x1, y1, z1));
      points.push(new THREE.Vector3(x2, y2, z2));
      const geometry = new THREE.BufferGeometry().setFromPoints(points);
      const material = new THREE.LineBasicMaterial({ color: 0xffffff });
      const line = new THREE.Line(geometry, material);
      scene.add(line);
    }

    function redistributeElements(left, right) {
      if (left.length > 21) {
        const redistributedElements = left.splice(21);
        right.push(...redistributedElements);
      } else if (right.length > 21) {
        const redistributedElements = right.splice(21);
        left.push(...redistributedElements);
      }
    }

    function connectLines(frameIndex) {
      const nodeConnections = [[0, 1], [1, 2], [2, 3], [3, 4], [0, 5], [5, 6], [6, 7], [7, 8], [5, 9], [9, 10], [10, 11], [11, 12], [9, 13], [13, 14], [14, 15], [15, 16], [13, 17], [17, 18], [18, 19], [19, 20], [0, 17]];
      var left = data[wordList[wordIndex]][frameIndex]['Left Hand Coordinates'];
      var right = data[wordList[wordIndex]][frameIndex]['Right Hand Coordinates'];

      redistributeElements(left, right);

      nodeConnections.forEach(function (node) {
        const u = node[0];
        const v = node[1];
        if (left[u] && left[v]) {
          const l1 = left[u];
          const l2 = left[v];
          drawLine(l1[0] * 50, l1[1] * -50, l1[2] * 50, l2[0] * 50, l2[1] * -50, l2[2] * 50);
        }
        if (right[u] && right[v]) {
          const r1 = right[u];
          const r2 = right[v];
          drawLine(r1[0] * 50, r1[1] * -50, r1[2] * 50, r2[0] * 50, r2[1] * -50, r2[2] * 50);
        }
      })
    }

    let clock = new THREE.Clock();
    let delta = 0;
    let interval = 1 / 500;
    console.log(sentenceList[sentenceIndex])
    var sentence = sentenceList[sentenceIndex].toLowerCase();
    var wordList = sentence.split(" ");

    function render() {
      requestAnimationFrame(render);
      delta += clock.getDelta();

      if (delta > interval) {
        delta = delta % interval;

        if (sentenceList.length > 0 && sentenceIndex < sentenceList.length) {

          console.log(wordList[wordIndex])
          var left = data[wordList[wordIndex]][frameIndex]['Left Hand Coordinates'];
          var right = data[wordList[wordIndex]][frameIndex]['Right Hand Coordinates'];

          for (var i = 0; i < left.length; i++) {
            drawPoint(left[i][0] * 50, left[i][1] * -50, left[i][2] * 50);
          }
          for (var i = 0; i < right.length; i++) {
            drawPoint(right[i][0] * 50, right[i][1] * -50, right[i][2] * 50);
          }
          connectLines(frameIndex);

          frameIndex++;
          if (frameIndex >= data[wordList[wordIndex]].length) {
            frameIndex = 0;
            wordIndex++;
          }
          if(wordIndex >= wordList.length) {
            console.log(clock.elapsedTime)
            while(clock.elapsedTime < (sentenceIndex + 1) * 3) {}
            console.log("YAY")
            wordIndex = 0;
            sentenceIndex++;
            sentence = sentenceList[sentenceIndex]
            sentence = sentence.toLowerCase();
            wordList = sentence.split(" ");
          }
        }
        renderer.render(scene, camera);
        scene.remove.apply(scene, scene.children);
      }
    }

    render();
  })

  camera.position.set(27.5, -30, 25);
  })
  .catch((e) => console.error(e));