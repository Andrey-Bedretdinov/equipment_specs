import React from "react"
import { Route, Routes } from "react-router-dom"
import NotFoundPage from "../NotFoundPage/NotFoundPage";
import ProjectCardsList from "../ProjectCardsList/ProjectCardsList";
import ProjectPage from "../../pages/ProjectPage/ProjectPage";

const AppRouter: React.FC = () => {
    return (
        <Routes>
            <Route path="/" element={<ProjectCardsList />} />
            <Route path="/projects/:project_id" element={<ProjectPage />} />
            <Route path="*" element={<NotFoundPage />} />
        </Routes>
    )
}

export default AppRouter;