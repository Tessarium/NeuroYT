import React, {Component, Fragment} from 'react'
import ReactDOM from 'react-dom'
import Header from './Header'
import ReactPlayer from 'react-player'
import DataProvider from './DataProvider'
import Table from './Table'
import RecogniseDetail from './Websocket'
import Images from './Img'
import "./index.css"


class App extends Component {
  render() {
    return (
            <Fragment>
                <Header title={'Распознавание объектов'} subtitle={'Демонстрационная версия'} />
                <ReactPlayer url='https://www.youtube.com/watch?v=Pc-IKzKADDM' playing />
                <DataProvider endpoint="api/recognise/"
                render={data => <Table data={data}  />} />
                <RecogniseDetail/>
                <Images/>
            </Fragment>
    )
  }
}

const root = document.querySelector('#app');
ReactDOM.render(<App />, root);