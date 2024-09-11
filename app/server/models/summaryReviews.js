import mongoose from 'mongoose';

const SummaryReview = mongoose.Schema({
    'name': Number,
    'tóm tắt': String,
    'reviews': String,
}, {
    collection: 'summary_reviews' 
})

const SummaryReviews = mongoose.model('summary_reviews', SummaryReview);

export default SummaryReviews;