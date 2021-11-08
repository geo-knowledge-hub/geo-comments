

import React, { Component } from "react";

import { Modal, Segment, Comment, Icon } from 'semantic-ui-react'

export class ListRatingModal extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <Modal
                closeIcon
                size={"large"}
                centered={false}
                dimmer={"blurring"}
                open={this.props.isModalOpen}
                onClose={this.props.modalHandler}
            >
                <Modal.Header>Community feedbacks</Modal.Header>
                <Modal.Content>

                    <Segment padded>
                        <Comment.Group size='large'>
                            <Comment>
                                <Comment.Avatar src='https://react.semantic-ui.com/images/avatar/small/matt.jpg' />
                                <Comment.Content>
                                    <Comment.Author as='a'>Matt</Comment.Author>
                                    <Comment.Metadata>
                                        <div>Today at 5:42PM</div>
                                        <div>
                                            <Icon name='star' />5 stars
                                        </div>
                                    </Comment.Metadata>
                                    <Comment.Text>How artistic!</Comment.Text>
                                </Comment.Content>
                            </Comment>

                            <Comment>
                                <Comment.Avatar src='https://react.semantic-ui.com/images/avatar/small/elliot.jpg' />
                                <Comment.Content>
                                    <Comment.Author as='a'>Elliot Fu</Comment.Author>
                                    <Comment.Metadata>
                                        <div>Yesterday at 12:30AM</div>
                                        <div>
                                            <Icon name='star' />4.2 stars
                                        </div>
                                    </Comment.Metadata>
                                    <Comment.Text>
                                        <p>This has been very useful for my research. Thanks as well!</p>
                                    </Comment.Text>
                                </Comment.Content>
                            </Comment>

                            <Comment>
                                <Comment.Avatar src='https://react.semantic-ui.com/images/avatar/small/joe.jpg' />
                                <Comment.Content>
                                    <Comment.Author as='a'>Joe Henderson</Comment.Author>
                                    <Comment.Metadata>
                                        <div>5 days ago</div>
                                        <div>
                                            <Icon name='star' />4.8 stars
                                        </div>
                                    </Comment.Metadata>
                                    <Comment.Text>Dude, this is awesome. Thanks so much</Comment.Text>
                                </Comment.Content>
                            </Comment>
                        </Comment.Group >
                    </Segment>
                </Modal.Content>
            </Modal>
        )
    }
}