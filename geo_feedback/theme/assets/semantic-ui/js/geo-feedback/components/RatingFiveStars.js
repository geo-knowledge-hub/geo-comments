import React, { Component } from "react";

import { Grid, Rating, List, Divider } from "semantic-ui-react";


export class RatingFiveStars extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        const { categories } = this.props;

        return (
            <>
                <List selection verticalAlign="middle" size={"big"} relaxed={"very"}>
                    {categories.map((category) => {
                        return (
                            <List.Item>
                                <List.Content floated="right">
                                    <Rating icon="star" defaultRating={0} maxRating={5} />
                                </List.Content>
                                <List.Content>
                                    <List.Header>{category}</List.Header>
                                </List.Content>
                            </List.Item>
                        );
                    })}
                </List>
            </>
        )
    }
}
