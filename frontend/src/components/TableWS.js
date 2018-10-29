import React from "react";
import ReactDOM from "react-dom";
import key from "weak-key";
import PropTypes from "prop-types";

function TableWS(data) {
  const element = (
    <div className="column">
      <h2 className="subtitle">
        Showing <strong>{data.length} items</strong>
      </h2>
      <table className="table is-striped">
        <thead>
          <tr>
            {Object.entries(data[0]).map(el => <th key={key(el)}>{el[0]}</th>)}
          </tr>
        </thead>
        <tbody>
          {data.map(el => (
            <tr key={el.id}>
              {Object.entries(el).map(el => <td key={key(el)}>{el[1]}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
  // highlight-next-line
  ReactDOM.render(element, document.getElementById('table'));
}

export default TableWS;


// export default tick;