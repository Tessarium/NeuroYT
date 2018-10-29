import React from 'react';
import Websocket from 'react-websocket';
import TableWS from './TableWS'
import ImagesWS from './ImagesWS'

  const resetable = Component => class extends React.Component {
  state = {key: 0};
  render() {
    return <Component
      {...this.props}
      reset={() => this.setState({key: this.state.key + 1})}
      key={this.state.key}
    />;
  }
};

  class RecogniseDetail extends React.Component {
      state = {
        data: [],
          loaded: false,
      };

    handleData(data) {
      let result = JSON.parse(data);
      // console.log(result);
        this.setState({ data: result, loaded: true });
        console.log(result);
        TableWS(result);
        ImagesWS();
    }
 
    render() {
      return (
        <div>
          <Websocket url='ws://195.154.242.132:9000'
              onMessage={this.handleData.bind(this)}/>
        </div>
      );
    }
  }

 
  export default RecogniseDetail;