/*
 * This file is part of GEO-Comments.
 * Copyright (C) 2022 GEO Secretariat.
 *
 * GEO-Comments is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import React from 'react';
import ReactDOM from 'react-dom';

import { FeedbackApp } from '@geo-knowledge-hub/geo-comments-react';


/**
 * Getting data
 */
const communityFeedbackDiv = document.getElementById('feedback-space-div');


/**
 * Render component
 */
export const renderComponent = (...args) => {
  if (communityFeedbackDiv) {
    ReactDOM.render(
      <FeedbackApp
        record={JSON.parse(communityFeedbackDiv.dataset.record)}
        userIsAuthenticated={JSON.parse(communityFeedbackDiv.dataset.userIsAuthenticated)}
        defaultQueryParams={JSON.parse(communityFeedbackDiv.dataset.defaultQueryConfig)}
      />,
      communityFeedbackDiv
    );
  }
};
