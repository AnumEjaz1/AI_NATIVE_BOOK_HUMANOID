import React, { createContext, useContext, useReducer, useEffect } from 'react';

// Define initial state
const initialState = {
  completedItems: [],
  viewedItems: [],
};

// Define actions
const actionTypes = {
  MARK_COMPLETED: 'MARK_COMPLETED',
  MARK_VIEWED: 'MARK_VIEWED',
  LOAD_PROGRESS: 'LOAD_PROGRESS',
  RESET_PROGRESS: 'RESET_PROGRESS',
};

// Reducer function
function progressReducer(state, action) {
  switch (action.type) {
    case actionTypes.MARK_COMPLETED:
      const completedSet = new Set(state.completedItems);
      if (action.payload) {
        completedSet.add(action.payload);
      }
      return {
        ...state,
        completedItems: Array.from(completedSet),
      };

    case actionTypes.MARK_VIEWED:
      const viewedSet = new Set(state.viewedItems);
      if (action.payload) {
        viewedSet.add(action.payload);
      }
      return {
        ...state,
        viewedItems: Array.from(viewedSet),
      };

    case actionTypes.LOAD_PROGRESS:
      return {
        ...state,
        completedItems: action.payload.completedItems || [],
        viewedItems: action.payload.viewedItems || [],
      };

    case actionTypes.RESET_PROGRESS:
      return initialState;

    default:
      return state;
  }
}

// Create context
const ProgressContext = createContext();

// Custom hook to use the progress context
export const useProgress = () => {
  const context = useContext(ProgressContext);
  if (!context) {
    throw new Error('useProgress must be used within a ProgressProvider');
  }
  return context;
};

// Progress provider component
export const ProgressProvider = ({ children }) => {
  const [state, dispatch] = useReducer(progressReducer, initialState);

  // Load progress from localStorage on initial render
  useEffect(() => {
    const savedProgress = localStorage.getItem('bookProgress');
    if (savedProgress) {
      try {
        const parsedProgress = JSON.parse(savedProgress);
        dispatch({ type: actionTypes.LOAD_PROGRESS, payload: parsedProgress });
      } catch (error) {
        console.error('Failed to load progress from localStorage:', error);
      }
    }
  }, []);

  // Save progress to localStorage whenever state changes
  useEffect(() => {
    try {
      const progressData = {
        completedItems: state.completedItems,
        viewedItems: state.viewedItems,
      };
      localStorage.setItem('bookProgress', JSON.stringify(progressData));
    } catch (error) {
      console.error('Failed to save progress to localStorage:', error);
    }
  }, [state]);

  const markCompleted = (item) => {
    dispatch({ type: actionTypes.MARK_COMPLETED, payload: item });
  };

  const markViewed = (item) => {
    dispatch({ type: actionTypes.MARK_VIEWED, payload: item });
  };

  const resetProgress = () => {
    dispatch({ type: actionTypes.RESET_PROGRESS });
  };

  const isCompleted = (item) => {
    return state.completedItems.includes(item);
  };

  const isViewed = (item) => {
    return state.viewedItems.includes(item);
  };

  const getProgressPercentage = (items) => {
    if (!items || items.length === 0) return 0;
    const completedCount = items.filter(item => isCompleted(item)).length;
    return Math.round((completedCount / items.length) * 100);
  };

  const value = {
    completedItems: state.completedItems,
    viewedItems: state.viewedItems,
    markCompleted,
    markViewed,
    resetProgress,
    isCompleted,
    isViewed,
    getProgressPercentage,
  };

  return (
    <ProgressContext.Provider value={value}>
      {children}
    </ProgressContext.Provider>
  );
};