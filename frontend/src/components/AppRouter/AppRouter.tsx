import React from "react"
import { Route, Routes } from "react-router-dom"
import NotFoundPage from "../NotFoundPage/NotFoundPage";
import ProjectCardsList from "../ProjectCardsList/ProjectCardsList";
import ProjectPage from "../../pages/ProjectPage/ProjectPage";
import CatalogKtsPage from "../../pages/CatalogKtsPage/CatalogKtsPage";
import CatalogUnitPage from "../../pages/CatalogUnitPage/CatalogUnitPage";
import CatalogItemPage from "../../pages/CatalogItemPage/CatalogItemPage";

const AppRouter: React.FC = () => {
    return (
        <Routes>
            <Route path="/" element={<ProjectCardsList />} />
            <Route path="/projects/:project_id" element={<ProjectPage />} />
            <Route path="/catalog/kts" element={<CatalogKtsPage />} />
            <Route path="/catalog/units" element={<CatalogUnitPage />} />
            <Route path="/catalog/items" element={<CatalogItemPage />} />
            <Route path="*" element={<NotFoundPage />} />
        </Routes>
    )
}

export default AppRouter;