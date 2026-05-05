import { useState } from "react";

function SurveyFormPage() {

  const [formData, setFormData] = useState({
    title: "",
    employeeName: "",
    department: "",
    riskCategory: "",
    surveyScore: "",
    status: "",
    description: "",
    aiAnalysis: "",
    createdBy: "",
  });

  const [errors, setErrors] = useState({});

  const handleChange = (e) => {

  const { name, value } = e.target;

  setFormData({
    ...formData,
    [name]: value,
  });

  setErrors({
    ...errors,
    [name]: "",
  });
};

  const validateForm = () => {

    let newErrors = {};

    if (!formData.title.trim()) {
      newErrors.title = "Title is required";
    }

    if (!formData.employeeName.trim()) {
      newErrors.employeeName = "Employee name is required";
    }

    if (!formData.department.trim()) {
      newErrors.department = "Department is required";
    }

    if (!formData.riskCategory.trim()) {
      newErrors.riskCategory = "Risk category is required";
    }

    if (!formData.surveyScore) {
      newErrors.surveyScore = "Survey score is required";
    }

    if (!formData.status.trim()) {
      newErrors.status = "Status is required";
    }

    if (!formData.description.trim()) {
      newErrors.description = "Description is required";
    }

    if (!formData.createdBy.trim()) {
      newErrors.createdBy = "Created by is required";
    }

    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {

    e.preventDefault();

    const isValid = validateForm();

    if (!isValid) {
      return;
    }

    console.log("Form Submitted:", formData);

    alert("Survey submitted successfully!");

    setFormData({
      title: "",
      employeeName: "",
      department: "",
      riskCategory: "",
      surveyScore: "",
      status: "",
      description: "",
      aiAnalysis: "",
      createdBy: "",
    });

    setErrors({});
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">

      <div className="max-w-4xl mx-auto bg-white shadow-2xl rounded-2xl p-8">

        <h1 className="text-4xl font-bold text-gray-800 mb-8 text-center">
          Risk Culture Survey Form
        </h1>

        <form onSubmit={handleSubmit} className="space-y-6">

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

            <div>
              <label className="block mb-2 font-semibold text-gray-700">
                Title
              </label>

              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter survey title"
              />

              {errors.title && (
                <p className="text-red-500 mt-1 text-sm">
                  {errors.title}
                </p>
              )}
            </div>

            <div>
              <label className="block mb-2 font-semibold text-gray-700">
                Employee Name
              </label>

              <input
                type="text"
                name="employeeName"
                value={formData.employeeName}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter employee name"
              />

              {errors.employeeName && (
                <p className="text-red-500 mt-1 text-sm">
                  {errors.employeeName}
                </p>
              )}
            </div>

          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

            <div>
              <label className="block mb-2 font-semibold text-gray-700">
                Department
              </label>

              <input
                type="text"
                name="department"
                value={formData.department}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter department"
              />

              {errors.department && (
                <p className="text-red-500 mt-1 text-sm">
                  {errors.department}
                </p>
              )}
            </div>

            <div>
              <label className="block mb-2 font-semibold text-gray-700">
                Risk Category
              </label>

              <input
                type="text"
                name="riskCategory"
                value={formData.riskCategory}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter risk category"
              />

              {errors.riskCategory && (
                <p className="text-red-500 mt-1 text-sm">
                  {errors.riskCategory}
                </p>
              )}
            </div>

          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

            <div>
              <label className="block mb-2 font-semibold text-gray-700">
                Survey Score
              </label>

              <input
                type="number"
                name="surveyScore"
                value={formData.surveyScore}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter survey score"
              />

              {errors.surveyScore && (
                <p className="text-red-500 mt-1 text-sm">
                  {errors.surveyScore}
                </p>
              )}
            </div>

            <div>
              <label className="block mb-2 font-semibold text-gray-700">
                Status
              </label>

              <select
                name="status"
                value={formData.status}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Select status</option>
                <option value="PENDING">PENDING</option>
                <option value="APPROVED">APPROVED</option>
              </select>

              {errors.status && (
                <p className="text-red-500 mt-1 text-sm">
                  {errors.status}
                </p>
              )}
            </div>

          </div>

          <div>
            <label className="block mb-2 font-semibold text-gray-700">
              Description
            </label>

            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="4"
              className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter description"
            />

            {errors.description && (
              <p className="text-red-500 mt-1 text-sm">
                {errors.description}
              </p>
            )}
          </div>

          <div>
            <label className="block mb-2 font-semibold text-gray-700">
              AI Analysis
            </label>

            <textarea
              name="aiAnalysis"
              value={formData.aiAnalysis}
              onChange={handleChange}
              rows="3"
              className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter AI analysis"
            />
          </div>

          <div>
            <label className="block mb-2 font-semibold text-gray-700">
              Created By
            </label>

            <input
              type="text"
              name="createdBy"
              value={formData.createdBy}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter creator name"
            />

            {errors.createdBy && (
              <p className="text-red-500 mt-1 text-sm">
                {errors.createdBy}
              </p>
            )}
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 rounded-xl transition duration-300"
          >
            Submit Survey
          </button>

        </form>

      </div>

    </div>
  );
}

export default SurveyFormPage;