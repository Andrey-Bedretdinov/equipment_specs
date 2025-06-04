import React from "react"
import { BrowserRouter, Route, Routes } from "react-router-dom"
import NotFoundPage from "../NotFoundPage/NotFoundPage";
import ProjectCardsList from "../ProjectCardsList/ProjectCardsList";

const AppRouter: React.FC = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<ProjectCardsList/>}/>
                <Route path="/projects/:project_id" element={<div>PENIS</div>}/>
                <Route path="*" element={<NotFoundPage/>}/>
            </Routes>
        </BrowserRouter>
    )
}

export default AppRouter;