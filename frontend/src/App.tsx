import { BrowserRouter } from 'react-router-dom'
import './App.css'
import AppRouter from './components/AppRouter/AppRouter'
import Navbar from './components/NavBar/NavBar'

function App() {

    return (
        <BrowserRouter>
            <Navbar />
            <div className='main'>
                <AppRouter />
            </div>
        </BrowserRouter>
    )
}

export default App