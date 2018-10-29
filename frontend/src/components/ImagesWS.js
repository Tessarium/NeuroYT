import React from "react";
import ReactDOM from "react-dom";
import key from "weak-key";
import PropTypes from "prop-types";
import Image from 'react-image';

function ImagesWS() {
  const element = (
        <table>
        <tbody>
        <tr>
          <td>
            {/*<img src='http://neuro.nulla.tech/static/images/in.png'></img>*/}
            <Image src={'http://neuro.nulla.tech/static/images/in.png' + '?' + new Date()}/>
          </td>
          <td>
            {/*<img src='http://neuro.nulla.tech/static/images/out.png'></img>*/}
            <Image src={'http://neuro.nulla.tech/static/images/out.png' + '?' + new Date()}/>
          </td>
        </tr>
        </tbody>
    </table>
  );
  // highlight-next-line
  ReactDOM.render(element, document.getElementById('images'));
}

export default ImagesWS;


// export default tick;