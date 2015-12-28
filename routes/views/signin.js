var keystone = require('keystone');

exports = module.exports = function(req, res) {

	var view = new keystone.View(req, res);
	var locals = res.locals;

	// locals.section is used to set the currently selected
	// item in the header navigation.
	backURL = req.header('Referer') || '/';
	if (req.user.authenticated)
    
  res.redirect(backURL);

};
