import React from "react";
import ReactDOM from 'react-dom';


const Images = () =>
    <div>
        <div id='timer'>
            <h2>It is {new Date().toLocaleTimeString()}.</h2>
        </div>
        <div id ='images'>
    <table>
        <tbody>
        <tr>
          <td>
            <img src='http://neuro.nulla.tech/static/images/in.png'></img>
          </td>
          <td>
            <img src='http://neuro.nulla.tech/static/images/out.png'></img>
          </td>
        </tr>
        </tbody>
    </table>
    </div></div>
;

function tick() {
  const element = (
    <div>
      <h2>It is {new Date().toLocaleTimeString()}.</h2>
    </div>
  );
  // highlight-next-line
  ReactDOM.render(element, document.getElementById('timer'));
}

setInterval(tick, 1000);

  export default Images;
