
import type { IKts } from "../../types/types";
import UnitCard from "../UnitCard/UnitCard";

interface UnitCardsListProps {
    units_list: IKts[];
    canDelete?: boolean;
}
const UnitCardsList: React.FC<UnitCardsListProps> = ({units_list, canDelete}) => {

    return (
        <>
            {units_list.map((unit) => 
                <UnitCard key={unit.id} unit={unit} canDelete={canDelete}/>
            )}
        </>
    )

}

export default UnitCardsList;