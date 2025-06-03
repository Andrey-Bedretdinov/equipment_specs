import './App.css'
import ProjectTree from './components/ProjectTree/ProjectTree'
import { projectsData } from './constants/projectsData'

function App() {

    return (
        <>
            <ProjectTree data={projectsData}/>
        </>
    )
}

export default App
