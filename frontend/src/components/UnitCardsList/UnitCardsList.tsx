
import type { IKts } from "../../types/types";
import UnitCard from "../UnitCard/UnitCard";

interface UnitCardsListProps {
    units_list: IKts[];
}
const UnitCardsList: React.FC<UnitCardsListProps> = ({units_list}) => {

    return (
        <>
            {units_list.map((unit) => 
                <UnitCard key={unit.id} unit={unit}/>
            )}
        </>
    )

}

export default UnitCardsList;